from flask import Flask
from home.views import home_blueprint, google_blueprint
from rest_api.views import api_blueprint
from rest_api.models import FileModel

DEBUG = True
app = Flask(import_name=__name__, static_url_path='')
app.secret_key = 'supersecret'


# Register blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(google_blueprint, url_prefix='/login')

FileModel.create_table(read_capacity_units=1, write_capacity_units=1)

# Start the server

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=DEBUG)
