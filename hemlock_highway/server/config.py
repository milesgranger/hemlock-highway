# -*- coding: utf-8 -*-

import os
import yaml


# The root directory of this repo.
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# check if there is a .secrets.yml file; for local development only.
if os.path.isfile(os.path.join(ROOT_DIR, '.secrets.yml')):
    with open(os.path.join(ROOT_DIR, '.secrets.yml')) as f:
        environment = yaml.load(f)

    # Set all the environment variables from .secrets.yml
    for key, value in environment.items():
        os.environ[key] = str(value).strip()

    print(os.environ)


class Config:

    ROOT_DIR    = ROOT_DIR
    DEBUG       = bool(int(os.getenv('DEBUG', 0)))
    HOST        = os.getenv('HOST', '127.0.0.1')
    PORT        = int(os.getenv('PORT', 5555))
    SECRET_KEY  = os.getenv('SECRET_KEY', 'super_secret')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth
    OAUTHLIB_INSECURE_TRANSPORT = int(os.getenv('OAUTHLIB_INSECURE_TRANSPORT', 0))
    OAUTHLIB_RELAX_TOKEN_SCOPE  = int(os.getenv('OAUTHLIB_RELAX_TOKEN_SCOPE', 1))
    GOOGLE_OAUTH_CLIENT_ID      = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET  = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
