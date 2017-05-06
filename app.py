import os
from flask import Flask
from home.views import home_blueprint

app = Flask(import_name=__name__, static_url_path='')

app.register_blueprint(home_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
