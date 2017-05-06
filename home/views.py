import boto3
import os
import sys
from flask.blueprints import Blueprint
from flask import render_template, request, flash, jsonify, current_app

home_blueprint = Blueprint(name='home_blueprint',
                           import_name=__name__,
                           template_folder='templates',
                           static_folder='static',
                           )

@home_blueprint.route('/')
def home_page():
    return render_template('home_index.html')


