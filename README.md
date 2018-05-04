# Hemlock Highway

[![Build Status](https://travis-ci.org/milesgranger/hemlock-highway.svg?branch=master)](https://travis-ci.org/milesgranger/hemlock-highway)
[![Coverage Status](https://coveralls.io/repos/github/milesgranger/hemlock-highway/badge.svg?branch=master)](https://coveralls.io/github/milesgranger/hemlock-highway?branch=master)
---

Development area for project Hemlock Highway

## Env setup:
```commandline
virtualenv -p $(which python3.6) venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools pip-tools
pip-sync
python -m hemlock_highway
```