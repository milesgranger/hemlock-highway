import os

from flask import Flask
from opplett.views import opplett_blueprint
from opplett.oauth_blueprints import google_blueprint
from rest_api.views import api_blueprint
from rest_api.utils import create_tables

DEBUG = True
app = Flask(import_name=__name__, static_url_path='')
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
