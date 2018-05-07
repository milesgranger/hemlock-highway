# -*- coding: utf-8 -*-

import json
import inspect
from flask import Blueprint, jsonify, request, make_response, Response
from hemlock_highway.ml.models import HemlockModelBase
from hemlock_highway.ml import models
from typing import Union

api_v1_blueprint = Blueprint(name='api_v1', import_name=__name__)


@api_v1_blueprint.route('/api/v1/available-models', methods=['GET'])
def available_models():
    """
    Return an array of strings with available models the client can use.
    """
    _models = [
        model for model in filter(lambda m: m.startswith('Hemlock'), dir(models))
        if issubclass(getattr(models, model), HemlockModelBase)
    ]
    return jsonify(_models)


@api_v1_blueprint.route('/api/v1/dump-model', methods=['POST'])
def dump_model():

    # To dump model, we need at least the name, optionally the config, otherwise default model init is used.
    model_name = request.form.get('model-name')
    model_conf = json.loads(request.form.get('model-config', '{}'))

    Model = get_model_by_name(model_name)

    if inspect.isclass(Model) and issubclass(Model, HemlockModelBase):
        # Initialize the model and dump it to the s3 bucket
        # TODO: Parameterize the dumping location.
        model = Model(**model_conf)  # type: HemlockModelBase
        model.dump(bucket='hemlock-highway-test', key='tests/model.pkl')
        return jsonify({'success': True})
    else:
        return Model


@api_v1_blueprint.route('/api/v1/model-parameters', methods=['GET'])
def model_parameters():

    model_name = request.args.get('model-name')

    Model = get_model_by_name(model_name)

    if inspect.isclass(Model) and issubclass(Model, HemlockModelBase):
        return jsonify({'success': True, 'parameters': Model.configurable_parameters()})
    else:
        return Model


def get_model_by_name(model_name: str) -> Union[HemlockModelBase, Response]:

    # If the name is None, we can't proceed
    if model_name is None:
        return make_response(jsonify({'success': False, 'error': 'model name required'}), 400)

    # Attempt to load model, otherwise it's a model name we don't know
    try:
        Model = getattr(models, model_name)
    except AttributeError:
        return make_response(jsonify({'success': False, 'error': f'model ({model_name}) not found'}), 404)

    return Model


