import os
import json

from flask import request, url_for, redirect, session, jsonify, current_app
from flask.views import MethodView
from oauth2client import client


class UserAuthorization(MethodView):
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

        if 'code' not in request.args:
            auth_uri = self.flow.step1_get_authorize_url()
            return redirect(auth_uri)

        else:
            auth_code = request.args.get('code')
            credentials = self.flow.step2_exchange(auth_code).to_json()  # Literally json, so here it is a string
            session['credentials'] = credentials
            credentials = json.loads(credentials)  # Convert literal json to dict
            current_app.logger.info('Type: {}'.format(type(credentials)))
            current_app.logger.info(credentials)

            user_email = credentials.get('id_token', {}).get('email', '')
            user_photo = credentials.get('id_token', {}).get('picture', '')
            user_given_name = credentials.get('id_token', {}).get('name', '')

            current_app.logger.info('Email: {}, Picture: {}, Given Name: {}'.format(user_email, user_photo, user_given_name))

            return jsonify({'login_status': 'successful',
                            'credentials': credentials
                            })

