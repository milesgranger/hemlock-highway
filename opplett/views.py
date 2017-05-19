import stripe
import os

from .utils import get_user_via_oauth
from .forms import UserNameForm, PaymentForm
from rest_api.dynamodb_models import UserModel

from flask.blueprints import Blueprint
from flask import (render_template, redirect, url_for,
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


@opplett_blueprint.route('/test')
def test():
    return render_template('profile_dashboard/dashboard.html')


@opplett_blueprint.route('/user/<username>')
def profile(username):
    """
    User Profile
    """

    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect

    dbuser = next(UserModel.query(hash_key=user.email), None)
    dbuser.bytes_stored += 100
    dbuser.save()

    if dbuser is not None:
        current_app.logger.info('Username: {}'.format(dbuser.username))
        if dbuser.username == username:
            payment_form = PaymentForm()
            return render_template('profile.html', user=dbuser, payment_form=payment_form, stripe_key = os.environ.get('STRIPE_PUBLISHABLE_KEY'))
        else:
            return 'We found you on google, but your username in the DB: {} does not match the one logged in with: {}'.format(dbuser.username, username)
    else:
        return 'Unable to locate you in the database'


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
            return redirect(url_for('opplett_blueprint.login'))
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
            return redirect(url_for('opplett_blueprint.profile', username=new_user.username))

    # If we made it here, user does not exist and has not been presented a form for creating a username
    return render_template('profile.html', user=user, username_form=form)








