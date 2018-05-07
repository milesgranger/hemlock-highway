# -*- coding: utf-8 -*-

import os
import boto3
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from flask.views import MethodView
from hemlock_highway.settings import PROJECT_CONFIG
from hemlock_highway.model_runner.runner import ModelRunner

app = Flask(__name__,
            root_path=os.path.dirname(__file__))

S3_CLIENT = boto3.client('s3', region_name=PROJECT_CONFIG.AWS_REGION)


class ModelRunnerAPI(MethodView):

    methods = ['POST']

    def post(self):
        # TODO: Tighten this up; update on job status, etc.
        model_location = request.form.get('model-location')
        bucket = model_location.split('/')[0]
        key = '/'.join(model_location.split('/')[1:])
        runner = ModelRunner(bucket=bucket, key=key)  # type: ModelRunner
        if runner.model.data_manager is None or not runner.model.data_manager.data_endpoint:
            return jsonify({'success': False,
                            'message': f'Loaded model at {model_location} does not have a valid DataManager'})
        return jsonify({'success': True, 'job-id': str(hashlib.md5(str(datetime.now()).encode('utf-8')))})


app.add_url_rule(rule='/train-model', view_func=ModelRunnerAPI.as_view('model_runner'))


if __name__ == '__main__':
    app.run()