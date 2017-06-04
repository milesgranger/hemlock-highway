import time
import ast
import random
from flask import current_app
from .models import get_redis_con
from flask_socketio import emit

"""
Classes for each SocketIO event which happens on the frontend.
"""


class NewConnection:
    
    def __init__(self, message: str) -> None:
        """
        Initialized by 'new-connection' SocketIO event
        Handle dealing with when a new client in connected
        """
        self.new_connection(message=message)

    @staticmethod
    def new_connection(message: str) -> None:
        """
        Notification of a new client connection
        """
        current_app.logger.info('Recieved connection from client: {}'.format(message))


class ModelSubmission:

    def __init__(self, data: dict) -> None:
        """
        Initialized by 'submit-model' SocketIO event
        Handle the submission and monitoring of a model tasks with SocketIO
        
        :param data: dict - Information to pass to compute worker via Redis 
        """
        self.redis = get_redis_con()
        self.job_id = random.randint(0, 10)
        self.submit_model(data=data)
        self.monitor_model()

    def submit_model(self, data: dict) -> None:
        """
        Submit a model for training, and yield updates from model training.
        """
        current_app.logger.info('Got request to run a model with parameters: {}'.format(data))
        self.redis.set(name=self.job_id, value={'model': 'linear_regression'})

    def monitor_model(self) -> None:
        """
        Ping Redis with the current job_id to emit the progress back to the client who submitted it.
        """
        while self.redis.exists(self.job_id):
            update = self.redis.get(self.job_id)
            update = ast.literal_eval(update.decode())
            current_app.logger.info('Result type: {update_type} - {update}'.format(update_type=type(update),
                                                                                   update=update)
                                    )
            emit('model-update', {'progress': update.get('progress', 0)})
            time.sleep(0.1)


