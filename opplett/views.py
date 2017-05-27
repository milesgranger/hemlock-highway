import stripe
import os
import time
import peewee as pw
import pickle
import json

from .utils import get_user_via_oauth, list_files_and_folders, get_s3fs, build_bread_crumbs
from .forms import UserNameForm, PaymentForm, NewDirectoryForm, RemoveDirectoryForm
from rest_api.models import UserModel, PaymentModel, POSTGRES_DB

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


@opplett_blueprint.route('/process-payment', methods=['POST'])
def process_payment():
    """
    Process a payment form. 
    """
    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect

    try:
        dbuser = UserModel.get(UserModel.email == user.email)
    except pw.DoesNotExist:
        dbuser = None

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
        charge = json.loads(json.dumps(charge.to_dict()))
        cleaned_charge = {}
        for k1, v1 in charge.items():
            if type(v1) != dict:
                cleaned_charge[k1] = v1
            else:
                for k2, v2 in v1.items():
                    cleaned_charge[k2] = v2

        current_app.logger.info('{}'.format(cleaned_charge))
        payment = PaymentModel.create(username=dbuser.username, **cleaned_charge)

        # Increment user balance
        dbuser.balance += payment.amount
        dbuser.save()


        # TODO: Save results of charge dictionary
        current_app.logger.info('Processed charge: {}'.format(cleaned_charge))
        flash('Payment of ${} succeeded!'.format(payment.amount / 100), 'success')
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
@opplett_blueprint.route('/user/<username>/<path:directory>')
def profile(username, directory=''):
    """
    User Profile
    """
    current_app.logger.info('Username {} requesting access to prifle page.'.format(username))

    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect to login via OAuth

    try:
        dbuser = UserModel.get(UserModel.email == user.email)
    except pw.DoesNotExist:
        dbuser = None

    if dbuser is not None:

        # TODO: Remove this
        dbuser.bytes_stored += 100
        dbuser.save()

        # User is verified by OAuth and they have created a username with us.
        if dbuser.username == username:

            start = time.time()
            payments = [payment for payment in PaymentModel.select().where(PaymentModel.username == dbuser.username)]
            current_app.logger.info('Payments: {}'.format(payments))
            current_app.logger.info('Queried database in {:.2f} seconds'.format(time.time() - start))
            start = time.time()
            folders, files = list_files_and_folders(dbuser.username, path=directory)
            current_app.logger.info('Queried files and folder on s3 in {:.2f} seconds'.format(time.time() - start))

            mkdir_form = NewDirectoryForm()
            mkdir_form.username.data = username

            return render_template('profile.html',
                                   user=dbuser,
                                   folders=folders,
                                   files=files,
                                   directory=directory,
                                   breadcrumbs=build_bread_crumbs(path=directory),
                                   payments=payments,
                                   payment_form=PaymentForm(),
                                   mkdir_form=NewDirectoryForm(),
                                   rmdir_form=RemoveDirectoryForm(),
                                   stripe_key=os.environ.get('STRIPE_PUBLISHABLE_KEY')
                                   )
        else:
            # User is logged in with OAuth and has a username with us but trying to access a profile which isn't theirs.
            flash('You are logged in as {} and do not have access to {}'.format(dbuser.username, username), 'info')
            return redirect(url_for('opplett_blueprint.profile', username=dbuser.username))
    else:
        # An unregistered user tried to access a profile page, need to redirect to login to create username
        flash('You need to register for your own account or login', 'info')
        return redirect(url_for('opplett_blueprint.login'))


@opplett_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect to OAuth login

    # Check if user exists in the database, if so, redirect to profile page without
    # form to create username.
    try:
        ddbuser = UserModel.get(UserModel.email == user.email)
    except pw.DoesNotExist:
        ddbuser = None

    if ddbuser is not None:
        current_app.logger.info('User {} is found in database, redirecting to profile page.'.format(ddbuser.username))
        return redirect(url_for('opplett_blueprint.profile', username=ddbuser.username))

    # Form processing if first time user has signed in.
    form = UserNameForm()
    if form.validate_on_submit():

        # Handle if username already exists.
        count = UserModel.select().where(UserModel.username == form.username.data).count()
        if count > 0:
            flash('Sorry the username <strong>{}</strong> already exists, please try a different one.'
                  .format(form.username.data),
                  'info')
            current_app.logger.info('Proposed username already exists in database: {}'.format(count))
            return redirect(url_for('opplett_blueprint.login'))
        # Store new username and redirect to profile page.
        else:
            current_app.logger.info('Saving new username: {}'.format(form.username.data))

            new_user = UserModel.create(username=form.username.data,
                                        email=user.email,
                                        name=user.name,
                                        profile_img=user.profile_img)
            flash('Your username: <strong>{}</strong> is accepted!'.format(form.username.data), 'success')
            current_app.logger.info('Processed proposed username: {}'.format(form.username.data))
            return redirect(url_for('opplett_blueprint.profile', username=new_user.username, vardirs=''))

    # If we made it here, user does not exist and has not been presented a form for creating a username
    return render_template('profile.html', user=user, username_form=form)


@opplett_blueprint.route('/new_directory', methods=['POST'])
def new_directory():
    """
    Create a new directory
    """

    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect
    dbuser = next(UserModel.query(hash_key=user.email), None)
    if dbuser is None:
        flash('Unable to process request, you were not found in the system!', 'warning')
        return redirect(url_for('opplett_blueprint.login'))

    form = NewDirectoryForm()
    if form.validate_on_submit():

        # Ensure that the directory user wants to delete exists
        if form.username.data == dbuser.username:
            fs = get_s3fs()
            # TODO: Ensure this bucket doesn't exist already
            new_dir = '{bucket}/{username}/{current_dir}{new_dir}'.format(bucket=os.environ.get('S3_BUCKET'),
                                                                          username=dbuser.username,
                                                                          current_dir=form.current_dir.data,
                                                                          new_dir=form.dir_name.data
                                                                          )
            current_app.logger.info('trying to make a new directory here: {}'.format(new_dir))
            fs.mkdir(new_dir)
            flash('Successfully made new directory!', 'success')
            return redirect(url_for('opplett_blueprint.profile',
                                    username=dbuser.username,
                                    directory='{current_dir}{new_dir}'.format(current_dir=form.current_dir.data,
                                                                              new_dir=form.dir_name.data))
                            )
        else:
            flash('Error making new directory, form username does not match authenticated username.', 'warning')

    return redirect(url_for('opplett_blueprint.profile', username=dbuser.username))




