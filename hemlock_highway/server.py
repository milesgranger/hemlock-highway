# -*- coding: utf-8 -*-

from flask import Flask, request
from hemlock_highway.config import Config
from hemlock_highway.api.v1 import api_v1_blueprint

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(api_v1_blueprint)


@app.route('/echo')
def echo():
    return request.args.get('word')
