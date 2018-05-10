# -*- coding: utf-8 -*-

import sys
import os
import yaml

repo_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Remove dev db if exists
db_file = os.path.join(repo_root, 'dev-database.db')
if os.path.isfile(db_file):
    os.remove(db_file)

# check if there is a .secrets.yml file; for local development only.
_path = os.path.join(repo_root, '.dev-env.yml')
if os.path.isfile(_path):
    print('INSERTING ENV Variables!')
    with open(_path) as f:
        environment = yaml.load(f)

    # Set all the environment variables from .secrets.yml
    for key, value in environment.items():
        os.environ[key] = str(value).strip()

    print('Loaded ENV variables from .dev-env.yml file')
else:
    raise EnvironmentError('Environment file not found not found!')


# Ensure the package is visible
if repo_root not in sys.path:
    sys.path.append(repo_root)

from hemlock_highway.server import app
from hemlock_highway.server.config import Config

config = Config()
app.config.from_object(config)

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, threaded=-config.DEBUG)
