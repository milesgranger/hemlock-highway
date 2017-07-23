import os
import json
from functools import wraps

from flask import request, url_for, redirect, session, jsonify, current_app
from flask.views import MethodView
from oauth2client import client


def login_required(func=None):
    """
    Decorator:
    Ensures current request involves an authenticated user
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        # If user is verified, process the request otherwise redirect to login view.
        if 'credentials' in session:
            return func(*args, **kwargs)
        else:
            # Redirect to wherever the UserAuthenticationAPI is registered.
            return redirect(url_for('opplett_blueprint.user-authorization'))

    return wrapper if callable(func) else login_required


class UserAuthorizationAPI(MethodView):
    """
    Manage user authorization via OAuth2
    Endpoint: /login
    Redirect to either oauth or user profile if authorized.
    """

    methods = ['GET', 'POST']

    def __init__(self):
        super(MethodView, self).__init__()

        # Google OAuth2 Client
        self.flow = client.OAuth2WebServerFlow(client_id=os.environ['OAUTH_GOOGLE_CLIENT_ID'],
                                               client_secret=os.environ['OAUTH_GOOGLE_CLIENT_SECRET'],
                                               scope=[
                                                   'https://www.googleapis.com/auth/userinfo.profile',
                                                   'https://www.googleapis.com/auth/userinfo.email'
                                               ],
                                               redirect_uri=url_for('opplett_blueprint.user-authorization', _external=True)
                                               )

    def get(self):
        """
        Authorized user, send to profile otherwise redirect to oauth url
        """

        # User is coming back with an authentication code from Google.
        if 'code' in request.args:
            auth_code = request.args.get('code')
            current_app.logger.info(session)
            credentials = self.flow.step2_exchange(auth_code).to_json()  # Literally json, so here it is a string
            credentials = json.loads(credentials)                        # Convert literal json to dict
            session['credentials'] = credentials

            user_email = credentials.get('id_token', {}).get('email', '')
            user_photo = credentials.get('id_token', {}).get('picture', '')
            user_given_name = credentials.get('id_token', {}).get('name', '')

            current_app.logger.info('Email: {}, Picture: {}, Given Name: {}'.format(user_email, user_photo, user_given_name))

            return jsonify({'login_status': 'successful',
                            'credentials': credentials
                            })

        # User has been previously authenticated, redirect to their profile.
        # TODO: do more verification of the tokens held in the credentials value found in session
        elif 'credentials' in session:
            return redirect(url_for('opplett_blueprint.user-profile'))

        # User is neither previously authenticated nor coming back from an OAuth consent, direct to OAuth consent.
        else:
            auth_uri = self.flow.step1_get_authorize_url()
            return redirect(auth_uri)

