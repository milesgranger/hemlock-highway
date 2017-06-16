import os
import time
import stripe
from flask import Flask
from flask_socketio import SocketIO

from opplett.views import opplett_blueprint
from opplett.socketio_hooks import NewConnection, ModelSubmission

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

# SocketIO
socketio = SocketIO(app)
socketio.on_event('new-connection', NewConnection)
socketio.on_event('submit-model', ModelSubmission)

# Start the server
if __name__ == '__main__':
    if DEBUG:
        from opplett.utils import create_tables
        time.sleep(3)  # Wait for other Postgres to get started before trying to create tables (local dev only)
        create_tables()
    socketio.run(app=app, host='0.0.0.0', port=int(os.environ.get('APP_PORT', 5555)), debug=DEBUG, use_reloader=DEBUG)
