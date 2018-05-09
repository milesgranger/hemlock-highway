# -*- coding: utf-8 -*-

from flask import Flask

from hemlock_highway.server.config import Config
from hemlock_highway.server.user_mgmt.models import db as user_db
from hemlock_highway.server.user_mgmt.auth import login_manager

# blueprints
from hemlock_highway.server.api import api_v1_blueprint
from hemlock_highway.server.ui import ui_blueprint
from hemlock_highway.server.user_mgmt import google_auth_blueprint, user_mgmt_blueprint


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Login
    login_manager.init_app(app)

    # Databases by blueprint
    user_db.init_app(app)

    # Create database tables
    with app.app_context():
        user_db.create_all()

    # Register blueprints
    app.register_blueprint(api_v1_blueprint)
    app.register_blueprint(ui_blueprint)
    app.register_blueprint(google_auth_blueprint, url_prefix='/google-login')  # Authorized url -> /google-login/google
    app.register_blueprint(user_mgmt_blueprint)

    return app


app = create_app()


@app.route('/health-check')
def health_check():
    return 'ahola', 200
