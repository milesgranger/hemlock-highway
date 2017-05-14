
from .models import User
from rest_api.dynamodb_models import UserModel

from flask.blueprints import Blueprint
from flask import render_template, redirect, url_for, current_app
from flask_dance.contrib.google import google


opplett_blueprint = Blueprint(name='opplett_blueprint',
                              import_name=__name__,
                              template_folder='templates',
                              static_folder='static',
                              )

@opplett_blueprint.route('/')
def home_page():
    return render_template('home_index.html')


@opplett_blueprint.route('/profile')
def profile():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    current_app.logger.info('Got Google Response: {}'.format(resp.text))

    user = User(resp.json(), source='google')

    ddbuser = next(UserModel.query(hash_key=user.email), None)

    if ddbuser is None:
        u = UserModel(email=user.email, username='milesg')
        u.save()
    else:
        current_app.logger.info('Got user from DynamoDB: email: {}, username: {}'.format(ddbuser.email,
                                                                                         ddbuser.username))

    return render_template('profile.html', user=user)


