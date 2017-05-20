import stripe
import os


from .utils import get_user_via_oauth, list_files_and_folders
from .forms import UserNameForm, PaymentForm
from rest_api.dynamodb_models import UserModel, PaymentModel

from flask.blueprints import Blueprint
from flask import (render_template, redirect, url_for, send_from_directory, jsonify,
                   current_app, request, flash)


opplett_blueprint = Blueprint(name='opplett_blueprint',
                              import_name=__name__,
                              template_folder='templates',
                              static_folder='static',
                              static_url_path='/opplett-static'
                              )


@opplett_blueprint.route('/')
def home():
    return render_template('home.html')


@opplett_blueprint.route('/payment', methods=['POST'])
def payment():
    """
    Process a payment form. 
    """
    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect

    dbuser = next(UserModel.query(hash_key=user.email), None)

    form = PaymentForm()
    if form.validate_on_submit():

        # Process payment
        customer = stripe.Customer.create(
            email=dbuser.email,
            source=request.form['stripeToken'],
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(form.data.get('payment_amount') * 100),  # stripe needs payment amounts in cents.
            currency='usd',
            description='Test charge'
        )

        # Save payment in DB
        payment = PaymentModel(username=dbuser.username,
                               payment_id=charge.to_dict().get('id'),
                               payment_details=charge.to_dict()
                               )
        payment.save()


        # Increment user balance
        dbuser.balance += charge.to_dict().get('amount') / 100  # Convert amount from stripes from cents to dollar amt.
        dbuser.save()


        # TODO: Save results of charge dictionary
        current_app.logger.info('Processed charge: {}'.format(charge.to_dict()))
        flash('Payment succeeded!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ), 'info')
    return redirect(url_for('opplett_blueprint.profile', username=dbuser.username))


# TODO: Fix this hack. :) change directory references in the html files.
@opplett_blueprint.route('/assets/<path:dirs>')
def redirect_files(dirs):
    d = os.path.join(os.path.dirname(__file__), 'templates', 'user_dashboard', 'assets', dirs)
    f = os.path.basename(d)
    d = os.path.dirname(d)
    return send_from_directory(d, f)

@opplett_blueprint.route('/test')
def test():

    return jsonify({'data': request.headers})

@opplett_blueprint.route('/user/<username>/')
@opplett_blueprint.route('/user/<username>')
@opplett_blueprint.route('/user/<username>/<directory>')
def profile(username, directory=''):
    """
    User Profile
    """

    current_app.logger.info('Username {} requesting access to prifle page.'.format(username))

    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect
    dbuser = next(UserModel.query(hash_key=user.email), None)


    # TODO: Remove this
    dbuser.bytes_stored += 100
    dbuser.save()


    if dbuser is not None:

        # User is verified by OAuth and they have created a username with us.
        if dbuser.username == username:
            payment_form = PaymentForm()
            payments = [payment._get_json() for payment in PaymentModel.query(hash_key=dbuser.username)]
            folders, files = list_files_and_folders(dbuser.username, path=directory)

            from .utils import get_s3fs
            fs = get_s3fs()
            fs.exists('s3://{bucket}/{username}/{vardirs}'.format(bucket=os.environ.get('S3_BUCKET'),
                                                                  username=username,
                                                                  vardirs=directory)
                      )

            #fs.mkdir('s3://{bucket}/{username}/test-folder'.format(bucket=os.environ.get('S3_BUCKET'),
            #                                                             username=username,
            #                                                             vardirs=vardirs)
            #         )

            return render_template('profile.html',
                                   user=dbuser,
                                   folders=folders,
                                   files=files,
                                   directory=['{dir}'.format(username=username, dir=dir)
                                              for dir in directory.split('/')],
                                   payments=payments,
                                   payment_form=payment_form,
                                   stripe_key=os.environ.get('STRIPE_PUBLISHABLE_KEY')
                                   )
        else:
            # User is logged in with OAuth and has a username with us but trying to access a profile which isn't theirs.
            return redirect(url_for('opplett_blueprint.profile', username=dbuser.username))
    else:
        current_app.logger.info('Current user found to be done in database, redirecting to login page.')
        # An unregistered user tried to access a profile page, need to redirect to login to create username
        return redirect(url_for('opplett_blueprint.login'))


@opplett_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect

    # Check if user exists in the database, if so, redirect to profile page without
    # form to create username.
    ddbuser = next(UserModel.query(hash_key=user.email), None)

    if ddbuser is not None:
        current_app.logger.info('User {} is found in database, redirecting to profile page.'.format(ddbuser.username))
        return redirect(url_for('opplett_blueprint.profile', username=ddbuser.username))

    # Form processing if first time user has signed in.
    form = UserNameForm()
    if form.validate_on_submit():

        # Handle if username already exists.
        if next(UserModel.username_index.query(hash_key=form.username.data), None) is not None:
            flash('Sorry the username <strong>{}</strong> already exists, please try a different one.'
                  .format(form.username.data),
                  'info')
            return redirect(url_for('opplett_blueprint.profile'))
        # Store new username and redirect to profile page.
        else:
            current_app.logger.info('Saving new username: {}'.format(form.username.data))
            new_user = UserModel(username=form.username.data,
                                 email=user.email,
                                 name=user.name,
                                 profile_img=user.profile_img)
            new_user.save()
            flash('Your username: <strong>{}</strong> is accepted!'.format(form.username.data), 'success')
            current_app.logger.info('Processed proposed username: {}'.format(form.username.data))
            return redirect(url_for('opplett_blueprint.profile', username=new_user.username, vardirs=''))

    # If we made it here, user does not exist and has not been presented a form for creating a username
    return render_template('profile.html', user=user, username_form=form)








