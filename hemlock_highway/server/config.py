# -*- coding: utf-8 -*-

import os
from hemlock_highway.settings import PROJECT_CONFIG

# The root directory of this repo.
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')







class Config:

    ROOT_DIR    = ROOT_DIR
    DEBUG       = bool(int(os.getenv('DEBUG', 0)))
    HOST        = os.getenv('HOST', '127.0.0.1')
    PORT        = int(os.getenv('PORT', 5555))
    SECRET_KEY  = os.getenv('SECRET_KEY', 'super_secret')

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', f"sqlite:///{PROJECT_CONFIG.REPO_ROOT_DIR}/dev-database.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth
    OAUTHLIB_INSECURE_TRANSPORT = int(os.getenv('OAUTHLIB_INSECURE_TRANSPORT', 0))
    OAUTHLIB_RELAX_TOKEN_SCOPE  = int(os.getenv('OAUTHLIB_RELAX_TOKEN_SCOPE', 1))
    GOOGLE_OAUTH_CLIENT_ID      = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET  = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
