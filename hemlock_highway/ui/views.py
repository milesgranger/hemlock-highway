# -*- coding: utf-8 -*-

from flask import redirect, url_for, current_app
from flask.blueprints import Blueprint
from flask_dance.contrib.google import google
from hemlock_highway.user_mgmt.user import User

ui_blueprint = Blueprint(__name__, import_name='ui')


@ui_blueprint.route('/login-google')
def login_google():

    if not google.authorized:
        current_app.logger.info(f'User not authorized! {google}')
        return redirect(url_for('google.login'))
    else:
        user = User.from_flask_dance_session(google)
        return f'You are {user.name} on Google.'
