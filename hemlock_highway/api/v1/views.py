# -*- coding: utf-8 -*-

import json
import boto3
from flask import Blueprint, jsonify, request, current_app, abort
from hemlock_highway.models import AbcHemlockModel
from hemlock_highway import models

api_v1_blueprint = Blueprint(__name__, import_name='api_v1')


@api_v1_blueprint.route('/api/v1/available-models')
def available_models():
    """
    Return an array of strings with available models the client can use.
    """
    _models = [
        model for model in filter(lambda m: m.startswith('Hemlock'), dir(models))
        if issubclass(getattr(models, model), AbcHemlockModel)
    ]
    return jsonify(_models)


@api_v1_blueprint.route('/api/v1/dump-model', methods=['POST'])
def dump_model():

    model_name = request.form.get('model-name')
    model_conf = json.loads(request.form.get('model-config', '{}'))
    if model_name is None:
        return jsonify({'success': False, 'error': 'model name required'}), 403

    current_app.logger.info(f'Model: {model_name} - Config: {model_conf}')
    Model = getattr(models, model_name)
    if Model is None:
        abort(404)
    model = Model(**model_conf)  # type: AbcHemlockModel
    model.dump(bucket='hemlock-highway-test', key='tests', name='model.pkl')
    return jsonify({'success': True})


@api_v1_blueprint.route('/api/v1/model-parameters', methods=['GET'])
def model_parameters():

    model_name = request.args.get('model-name')
    if model_name is None:
        abort(403)

    Model = getattr(models, model_name)  # type: AbcHemlockModel
    if Model is None:
        abort(403)
    return jsonify({'success': True, 'parameters': Model.configurable_parameters()})






