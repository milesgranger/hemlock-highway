from flask import current_app
from .models import get_redis_con

def new_connection(message):
    current_app.logger.info('Recieved connection from client: {}'.format(message))


def submit_model(data):
    """
    Submit a model for training 
    """
    current_app.logger.info('Got request to run a model with parameters: {}'.format(data))
    redis_con = get_redis_con()
    redis_con.set(name='01', value={'model': 'linear_regression'})



