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
from flask.views import View


opplett_blueprint = Blueprint(name='opplett_blueprint',
                              import_name=__name__,
                              template_folder='templates',
                              static_folder='static',
                              static_url_path='/opplett-static'
                              )


class HomeView(View):
    """View for the home page"""

    methods = ['GET']

    def dispatch_request(self):
        return render_template('home.html')
opplett_blueprint.add_url_rule(rule='/', view_func=HomeView.as_view('home'))


class PaymentView(View):
    """
    Handle the payment of a user account balance. 
    """

    methods = ['POST', ]

    def dispatch_request(self):
        """
        Handle dispatching of a payment request.
        """

        # Get google info about user
        user = get_user_via_oauth()
        if not hasattr(user, 'email'):
            return user  # This is a redirect

        try:
            self.dbuser = UserModel.get(UserModel.email == user.email)
        except pw.DoesNotExist:
            self.dbuser = None

        self.process_payment_request()
        return redirect(url_for('opplett_blueprint.profile', username=self.dbuser.username))

    def process_payment_request(self):
        """
        Process a payment form. 
        """
        form = PaymentForm()
        if form.validate_on_submit():
            self.process_validated_form(form)
        else:
            # There are errors if the form is not valid, flash messages before being redirected.
            for field, errors in form.errors.items():
                for error in errors:
                    flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'info')

    def process_validated_form(self, form):
        """
        Process a validated form (the user has submitted a valid payment form via Stripe)
        :param form: wtforms.Form - Validated form
        :return: None
        """
        customer = stripe.Customer.create(
            email=self.dbuser.email,
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
        cleaned_charge = self.clean_charge_data(charge)

        payment = PaymentModel.create(username=self.dbuser.username, **cleaned_charge)

        # Increment user balance
        self.dbuser.balance += payment.amount
        self.dbuser.save()

        # TODO: Save results of charge dictionary
        current_app.logger.info('Processed charge: {}'.format(cleaned_charge))
        flash('Payment of ${} succeeded!'.format(payment.amount / 100), 'success')

    def clean_charge_data(self, charge):
        """
        The data comming from stripe.Charge.create(...) can be messy.
        This 'flattens' a nested dictionary.
        :param charge: result of stripe.Charge.create(...) method.
        :return: a 'flattened' dictionary.
        """
        cleaned_charge = {}
        for k1, v1 in charge.items():
            if type(v1) != dict:
                cleaned_charge[k1] = v1
            else:
                for k2, v2 in v1.items():
                    cleaned_charge[k2] = v2

        current_app.logger.info('{}'.format(cleaned_charge))
        return cleaned_charge
opplett_blueprint.add_url_rule('/process-payment', view_func=PaymentView.as_view('process_payment'))


class ProfileView(View):
    """
    View for Profile page
    """

    methods = ['GET', ]

    def dispatch_request(self, username, directory=''):
        return self.profile(username, directory)


    def profile(self, username, directory):
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
profile_view = ProfileView.as_view('profile')
opplett_blueprint.add_url_rule('/user/<username>/', view_func=profile_view)
opplett_blueprint.add_url_rule('/user/<username>', view_func=profile_view)
opplett_blueprint.add_url_rule('/user/<username>/<path:directory>', view_func=profile_view)


class LoginView(View):

    def dispatch_request(self):
        return self.login()

    def login(self):

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
opplett_blueprint.add_url_rule('/login', view_func=LoginView.as_view('login'))


class NewDirectoryView(View):

    methods = ['POST', ]

    def dispatch_request(self):
        return self.new_directory()

    def new_directory(self):
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
opplett_blueprint.add_url_rule('/new-directory', view_func=NewDirectoryView.as_view('new_directory'))



