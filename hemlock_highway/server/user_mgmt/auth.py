# -*- coding: utf-8 -*-

from flask import redirect, url_for, Blueprint, current_app
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound

from hemlock_highway.server.config import Config
from hemlock_highway.server.user_mgmt.models import db

login_manager = LoginManager()

config = Config()

# OAuth blueprints
google_auth_blueprint = make_google_blueprint(client_id=config.GOOGLE_OAUTH_CLIENT_ID,
                                              client_secret=config.GOOGLE_OAUTH_CLIENT_SECRET,
                                              )

user_mgmt_blueprint = Blueprint('user_mgmt', __name__)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(250), unique=True)


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


google_auth_blueprint.backend = SQLAlchemyBackend(model=OAuth, session=db.session, user=current_user)



@oauth_authorized.connect_via(google_auth_blueprint)
def google_logged_in(google_auth_blueprint, token):
    blueprint = google_auth_blueprint

    if not token:
        current_app.logger.warn('Empty token!')
        return False



    account_info = google_auth_blueprint.session.get('/oauth2/v1/userinfo?alt=json')

    if not account_info.ok:
        raise IOError('Unable to get Google info on user')

    account_info = account_info.json()
    name = account_info.get('name')
    picture = account_info.get('picture')
    gender = account_info.get('gender')
    locale = account_info.get('locale')
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
        user = User(
            username=name
        )
        oauth.user = user

        db.session.add_all([user, oauth])
        db.session.commit()

        login_user(user)

    current_app.logger.info('Successfully logged in!')

    # Disable flask-dance default of saving OAuth token
    return False


@user_mgmt_blueprint.route('/check-login')
@login_required
def index():
    return '<h1>You are logged in as {}</h1>'.format(current_user.username)

@user_mgmt_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
