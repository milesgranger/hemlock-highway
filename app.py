import os

import stripe

from flask import Flask

from opplett.views import opplett_blueprint
from rest_api.oauth import google_blueprint
from rest_api.utils import create_tables
from rest_api.views import api_blueprint

DEBUG = os.environ.get('DEBUG', True)


# Stripe Payment setup
stripe_keys = {
    'secret_key': os.environ.get('STRIPE_SECRET_KEY'),
    'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY')
}
stripe.api_key = stripe_keys['secret_key']


# Application definition
app = Flask(import_name=__name__,
            static_url_path='/base-static',
            static_folder='static',
            )
app.secret_key = os.environ.get('SECRET_KEY')


# Register blueprints
app.register_blueprint(opplett_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(google_blueprint, url_prefix='/login')


# Start the server
if __name__ == '__main__':
    if DEBUG:
        create_tables()
    app.run(host='0.0.0.0', port=5555, debug=DEBUG)
