# -*- coding: utf-8 -*-

from setuptools import setup


_version = "0.0.1"

_requirements = []
with open('requirements.txt', 'r') as f:
    _requirements = [line.strip() for line in f if not (line.startswith('#') or line.startswith('--'))]

setup(
    name='hemlock-highway',
    version=_version,
    packages=['hemlock_highway'],
    author='Miles Granger',
    author_email='miles59923@gmail.com',
    description="Machine Learning Interface",
    install_requires=_requirements,
    test_suite='hemlock_highway.tests'
)
