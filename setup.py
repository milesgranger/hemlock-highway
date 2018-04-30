# -*- coding: utf-8 -*-

from setuptools import setup
from hemlock_highway import __version__


with open('requirements.txt', 'r') as f:
    install_requirements = [line.strip() for line in f if not (line.startswith('#') or line.startswith('--'))]

setup(
    name='hemlock-highway',
    version=__version__,
    packages=['hemlock_highway'],
    author='Miles Granger',
    author_email='miles59923@gmail.com',
    description="Machine Learning Interface",
    install_requires=install_requirements,
    test_suite='hemlock_highway.tests'
)
