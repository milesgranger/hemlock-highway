# -*- coding: utf-8 -*-

import os


class Config:

    DEBUG   = os.getenv('DEBUG', False)
    HOST    = os.getenv('HOST', '0.0.0.0')
    PORT    = os.getenv('PORT', 5555)
    ROOT_DIR= os.path.join(os.path.abspath(os.path.abspath(__file__)), '..')
