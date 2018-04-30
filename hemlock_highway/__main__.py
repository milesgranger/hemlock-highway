# -*- coding: utf-8 -*-

from hemlock_highway.app import app
from hemlock_highway.config import Config

config = Config()

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, threaded=-config.DEBUG)
