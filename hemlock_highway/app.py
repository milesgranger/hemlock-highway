# -*- coding: utf-8 -*-

import importlib
from flask import Flask, request, jsonify
from hemlock_highway.config import Config
from hemlock_highway.models import AbcHemlockModel


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/available-models')
def available_models():
    """
    Return an array of strings with available models the client can use.
    """
    module = importlib.import_module('hemlock_highway.models')
    models = [
        model for model in filter(lambda m: m.startswith('Hemlock'), dir(module))
        if issubclass(getattr(module, model), AbcHemlockModel)
    ]
    return jsonify(models)


@app.route('/echo')
def echo():
    return request.args.get('word')
