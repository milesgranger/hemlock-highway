# -*- coding: utf-8 -*-

import os
from flask import redirect, url_for, current_app, render_template
from flask.blueprints import Blueprint
from flask_dance.contrib.google import google
from hemlock_highway.server.user_mgmt.user import User

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

ui_blueprint = Blueprint(name='ui',
                         import_name=__name__,
                         template_folder=os.path.join(MODULE_PATH, 'templates'),
                         static_folder=os.path.join(MODULE_PATH, 'static'),
                         static_url_path='/static-ui')


@ui_blueprint.route('/')
def home_page():
    return render_template('index.html')

@ui_blueprint.route('/login-google')
def login_google():

    if not google.authorized:
        current_app.logger.info(f'User not authorized! {google}')
        return redirect(url_for('google.login'))
    else:
        user = User.from_flask_dance_session(google)
        return f'You are {user.name} on Google.'
