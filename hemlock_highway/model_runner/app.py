# -*- coding: utf-8 -*-

import os
import boto3
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from flask.views import MethodView
from hemlock_highway.settings import PROJECT_CONFIG
from hemlock_highway.ml.models import AbcHemlockModel

app = Flask(__name__,
            root_path=os.path.dirname(__file__))

S3_CLIENT = boto3.client('s3', region_name=PROJECT_CONFIG.AWS_REGION)


class ModelRunner(MethodView):

    methods = ['POST']

    def post(self):
        # TODO: Tighten this up; update on job status, etc.
        model_location = request.form.get('model-location')
        bucket = model_location.split('/')[0]
        key = '/'.join(model_location.split('/')[1:])
        model = AbcHemlockModel.load(bucket=bucket, key=key)  # type: AbcHemlockModel
        if model.data_manager is None or not model.data_manager.data_endpoint:
            return jsonify({'success': False,
                            'message': f'Loaded model at {model_location} does not have a valid DataManager'})
        model.data_manager.load()
        X, y = model.data_manager.X, model.data_manager.y
        model.fit(X, y)
        return jsonify({'success': True, 'job-id': str(hashlib.md5(str(datetime.now()).encode('utf-8')))})


app.add_url_rule(rule='/train-model', view_func=ModelRunner.as_view('model_runner'))


if __name__ == '__main__':
    app.run()