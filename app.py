from flask import Flask
from home.views import home_blueprint
from rest_api.views import api_blueprint

app = Flask(import_name=__name__, static_url_path='')

# Register blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(api_blueprint)

# Start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
