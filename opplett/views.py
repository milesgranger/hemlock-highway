import stripe
import os

from .utils import get_user_via_oauth
from .forms import UserNameForm, PaymentForm
from rest_api.dynamodb_models import UserModel

from flask.blueprints import Blueprint
from flask import render_template, redirect, url_for, current_app, request, flash




opplett_blueprint = Blueprint(name='opplett_blueprint',
                              import_name=__name__,
                              template_folder='templates',
                              static_folder='static',
                              )

@opplett_blueprint.route('/')
def home_page():
    return render_template('home_index.html')


@opplett_blueprint.route('/payment', methods=['POST'])
def payment():
    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect

    dbuser = next(UserModel.query(hash_key=user.email), None)

    form = PaymentForm()
    if form.validate_on_submit():

        current_app.logger.info('Got payment amount: {}'.format(form.data.get('payment_amount')))

        customer = stripe.Customer.create(
            email=dbuser.email,
            source=request.form['stripeToken'],
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(form.data.get('payment_amount') * 100),
            currency='usd',
            description='Test charge'
        )
        flash('Payment succeeded!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ), 'info')
    return redirect(url_for('opplett_blueprint.profile', username_or_id=dbuser.username))


@opplett_blueprint.route('/user/<username_or_id>')
def profile(username_or_id):
    """If first time user has signed in, create a username"""

    # Get google info about user
    user = get_user_via_oauth()
    if not hasattr(user, 'email'):
        return user  # This is a redirect

    dbuser = next(UserModel.query(hash_key=user.email), None)

    if dbuser is not None:
        if dbuser.email == user.email:
            payment_form = PaymentForm()
            return render_template('profile.html', user=user, payment_form=payment_form, stripe_key = os.environ.get('STRIPE_PUBLISHABLE_KEY'))
        else:
            return 'We found you on google, but your username in the DB: {} does not match the one provided: {}'.format(dbuser.username, username_or_id)
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
        return redirect(url_for('opplett_blueprint.profile', username_or_id=ddbuser.username))

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
            new_user = UserModel(username=form.username.data, email=user.email)
            new_user.save()
            flash('Your username: <strong>{}</strong> is accepted!'.format(form.username.data), 'success')
            current_app.logger.info('Processed proposed username: {}'.format(form.username.data))
            return redirect(url_for('opplett_blueprint.profile', username_or_id=new_user.username))

    # If we made it here, user does not exist and has not been presented a form for creating a username
    return render_template('profile.html', user=user, username_form=form)








