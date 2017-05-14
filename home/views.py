import boto3
import os
import sys
from flask.blueprints import Blueprint
from flask import render_template, redirect, url_for, current_app
from flask_dance.contrib.google import make_google_blueprint, google


class User:

    def __init__(self, data):
        self.name = data.get('name')
        self.profile_img = data.get('picture')
        self.email = data.get('email')


google_blueprint = make_google_blueprint(
    client_id=os.environ.get('OAUTH_GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('OAUTH_GOOGLE_CLIENT_SECRET'),
    scope=['profile', 'email'],
    redirect_to='home.profile'
)


home_blueprint = Blueprint(name='home_blueprint',
                           import_name=__name__,
                           template_folder='templates',
                           static_folder='static',
                           )

@home_blueprint.route('/')
def home_page():
    return render_template('home_index.html')

@home_blueprint.route('/profile/<user>')
def profile(user):
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    current_app.logger.info('Got Google Response: {}'.format(resp.text))

    user = User(resp.json())

    return render_template('profile.html', user=user)


