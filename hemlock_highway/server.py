# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for
from flask_dance.contrib.google import google
from hemlock_highway.config import Config
from hemlock_highway.user_mgmt import google_auth_blueprint, User

# blueprints
from hemlock_highway.api.v1 import api_v1_blueprint


app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(api_v1_blueprint)
app.register_blueprint(google_auth_blueprint, url_prefix='/google-login')


@app.route('/login-google')
def login_google():
    if not google.authorized:
        return redirect(url_for('google.login'))
    else:
        user = User.from_flask_dance_session(google)
        return f'You are {user.name} on Google.'


@app.route('/echo')
def echo():
    return request.args.get('word')
