# -*- coding: utf-8 -*-

import sys
import os

# Ensure the package is visible
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
if PATH not in sys.path:
    sys.path.append(PATH)

from hemlock_highway.server import app
from hemlock_highway.server.config import Config

config = Config()

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, threaded=-config.DEBUG)
