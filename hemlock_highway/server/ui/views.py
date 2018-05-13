# -*- coding: utf-8 -*-

import os
from flask import render_template, jsonify
from flask.blueprints import Blueprint
from flask_login import login_required, current_user
from hemlock_highway.server.user_mgmt.models import MachineLearningModel, db, User

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

ui_blueprint = Blueprint(name='ui',
                         import_name=__name__,
                         template_folder=os.path.join(MODULE_PATH, 'templates'),
                         static_folder=os.path.join(MODULE_PATH, 'static'),
                         static_url_path='/static-ui')


@ui_blueprint.route('/')
def index():
    return render_template('index.html')


@ui_blueprint.route('/dashboard')
@login_required
def dashboard():
    model = MachineLearningModel(user_id=current_user.id,
                                 name='My awesome model',
                                 trained=False,
                                 size_bytes=123)
    db.session.add(model)
    db.session.commit()

    context = {}
    context['current_user'] = current_user

    models = db.session.query(MachineLearningModel).join(User).filter(User.id == current_user.id).all()
    context['models'] = models

    return render_template('dashboard.html', **context)
