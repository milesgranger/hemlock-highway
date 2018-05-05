# -*- coding: utf-8 -*-

import os


class ProjectConfig:

    # Directories
    REPO_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    HEMLOCK_HIGHWAY_MODULE_ROOT_DIR = os.path.join(REPO_ROOT_DIR, 'hemlock_highway')
    TEST_ROOT_DIR = os.path.join(REPO_ROOT_DIR, 'tests')
    TEST_DATA_DIR = os.path.join(TEST_ROOT_DIR, 'data')

    AWS_REGION = 'eu-west-1'


PROJECT_CONFIG = ProjectConfig()
