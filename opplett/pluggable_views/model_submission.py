import os

from opplett.models import get_redis_con
from flask import request, jsonify, current_app
from flask.views import MethodView


class ModelSubmissionAPI(MethodView):
    """
    View to take model submission requests and send off to get processed.
    Takes GET requests to provide updates to the running job.
    """
    methods = ['GET', 'POST']

    def get(self):
        return jsonify({'echo': True})

    def post(self):
        data = request.get_json()
        current_app.logger.info('Submitting model request: {}'.format(data))
        self.submit_model_request(data=data)
        return jsonify({'job-id': 23493802})

    def submit_model_request(self, data):
        """Submit json data of model architecture to process"""
        redis = get_redis_con()
        redis.set('job-id-123', data)
        if not os.environ.get('DEBUG', False):
            # TODO (Miles) Start submit the job to the Batch pipeline with corresponding job code.
            pass
        return True
