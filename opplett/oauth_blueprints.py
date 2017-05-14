import os
from flask_dance.contrib.google import make_google_blueprint


google_blueprint = make_google_blueprint(
    client_id=os.environ.get('OAUTH_GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('OAUTH_GOOGLE_CLIENT_SECRET'),
    scope=['profile', 'email'],
    redirect_to='opplett_blueprint.profile'
)