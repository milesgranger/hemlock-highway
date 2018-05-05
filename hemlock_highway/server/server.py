# -*- coding: utf-8 -*-

from flask import Flask, request

from hemlock_highway.server.config import Config

# blueprints
from hemlock_highway.server.api import api_v1_blueprint
from hemlock_highway.server.ui import ui_blueprint
from hemlock_highway.server.user_mgmt import google_auth_blueprint


app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(api_v1_blueprint)
app.register_blueprint(ui_blueprint)
app.register_blueprint(google_auth_blueprint, url_prefix='/google-login')


@app.route('/health-check')
def health_check():
    return 'ahola', 200
