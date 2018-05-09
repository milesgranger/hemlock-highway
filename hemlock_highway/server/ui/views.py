# -*- coding: utf-8 -*-

import os
from flask import redirect, url_for, current_app, render_template
from flask.blueprints import Blueprint
from flask_dance.contrib.google import google
from flask_login import login_required, current_user

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

ui_blueprint = Blueprint(name='ui',
                         import_name=__name__,
                         template_folder=os.path.join(MODULE_PATH, 'templates'),
                         static_folder=os.path.join(MODULE_PATH, 'static'),
                         static_url_path='/static-ui')


@ui_blueprint.route('/')
def home_page():
    return render_template('index.html')



@ui_blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user.username)
