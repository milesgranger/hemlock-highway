# -*- coding: utf-8 -*-

from flask_dance.contrib.google import make_google_blueprint
from hemlock_highway.config import Config

config = Config()

google_auth_blueprint = make_google_blueprint(client_id=config.GOOGLE_CLIENT_ID,
                                              client_secret=config.GOOGLE_CLIENT_SECRET,
                                              )
