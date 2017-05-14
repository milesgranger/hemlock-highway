
from .models import User
from rest_api.dynamodb_models import UserModel

from flask.blueprints import Blueprint
from flask import render_template, redirect, url_for, current_app, request, flash
from flask_dance.contrib.google import google

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class UserNameForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(message='Required.')])


opplett_blueprint = Blueprint(name='opplett_blueprint',
                              import_name=__name__,
                              template_folder='templates',
                              static_folder='static',
                              )

@opplett_blueprint.route('/')
def home_page():
    return render_template('home_index.html')


@opplett_blueprint.route('/create_username')
def create_username():
    """If first time user has signed in, create a username"""
    proposed_username = request.args.get('username')
    if next(UserModel.username_index.query(hash_key=proposed_username), None) is not None:
        pass


@opplett_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():

    # Ensure user is validated first.
    try:
        if not google.authorized:
            return redirect(url_for('google.login'))
        resp = google.get('/oauth2/v2/userinfo')
    except:
        return redirect(url_for('google.login'))

    user = User(resp.json(), source='google')

    form = UserNameForm()
    if form.validate_on_submit():

        if next(UserModel.username_index.query(hash_key=form.username.data), None) is not None:
            flash('Sorry the username <strong>{}</strong> already exists, please try a different one.'
                  .format(form.username.data),
                  'info')
        else:
            current_app.logger.info('Saving new username: {}'.format(form.username.data))
            new_user = UserModel(username=form.username.data, email=user.email)
            new_user.save()
            flash('Your username: <strong>{}</strong> is accepted!'.format(form.username.data), 'success')
        current_app.logger.info('Got proposed username: {}'.format(form.username.data))
        return redirect(url_for('opplett_blueprint.profile'))

    current_app.logger.info('Got Google Response: {}'.format(resp.text))

    ddbuser = next(UserModel.query(hash_key=user.email), None)

    return render_template('profile.html', user=user, form=form if ddbuser is None else None)


