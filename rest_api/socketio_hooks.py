import time
import ast
import random
from flask import current_app
from .models import get_redis_con
from flask_socketio import emit


def new_connection(message: str) -> None:
    """
    Notification of a new client connection
    """
    current_app.logger.info('Recieved connection from client: {}'.format(message))


def submit_model(data: dict) -> None:
    """
    Submit a model for training, and yield updates from model training.
    """
    job = random.randint(0, 10)
    current_app.logger.info('Got request to run a model with parameters: {}'.format(data))
    redis_con = get_redis_con()
    redis_con.set(name=job, value={'model': 'linear_regression'})

    while redis_con.exists(job):
        update = redis_con.get(job)
        update = ast.literal_eval(update.decode())
        current_app.logger.info('Result type: {update_type} - {update}'.format(update_type=type(update), update=update))
        emit('model-update', {'progress': update.get('progress', 0)})
        time.sleep(0.1)



