# -*- coding: utf-8 -*-

from flask import redirect, url_for, Blueprint, current_app
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound

from hemlock_highway.server.config import Config
from hemlock_highway.server.user_mgmt.models import db, User, OAuth

login_manager = LoginManager()

config = Config()

# OAuth blueprints, basically provides endpoint for logging in.
google_auth_blueprint = make_google_blueprint(client_id=config.GOOGLE_OAUTH_CLIENT_ID,
                                              client_secret=config.GOOGLE_OAUTH_CLIENT_SECRET,
                                              scope=['profile', 'email']
                                              )

# OAuth blueprints have a backend to store the token of the current user, allowing to logout and use with Flask-Login
google_auth_blueprint.backend = SQLAlchemyBackend(model=OAuth, session=db.session, user=current_user)

# Views for user managment routes, like '/logout' or other user specific controls
user_mgmt_blueprint = Blueprint('user_mgmt', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@oauth_authorized.connect_via(google_auth_blueprint)
def google_logged_in(blueprint, token):
    """
    Handle a google login - Either login an existing user, or create a user in the database.
    """
    if not token:
        current_app.logger.warn('Empty token!')
        return False

    account_info = blueprint.session.get('/oauth2/v1/userinfo?alt=json')

    if not account_info.ok:
        raise IOError('Unable to get Google info on user')

    account_info = account_info.json()
    current_app.logger.info(account_info)
    name_first = account_info.get('name') or account_info.get('given_name')
    name_last = account_info.get('family_name')
    email = account_info['email']
    picture = account_info.get('picture')
    gender = account_info.get('gender')
    locale = account_info.get('locale')
    external_profile_page = account_info.get('link')
    provider_user_id = str(account_info['id'])

    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=provider_user_id
    )

    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=provider_user_id,
            token=token
        )

    if oauth.user:
        login_user(oauth.user)
    else:
        user = User(email=email)
        oauth.user = user

        db.session.add_all([user, oauth])
        db.session.commit()

        login_user(user)

    current_app.logger.info('Successfully logged in!')

    # Disable flask-dance default of saving OAuth token
    return False

@user_mgmt_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('ui.index'))
