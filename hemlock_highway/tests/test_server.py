# -*- coding: utf-8 -*-

import unittest
from hemlock_highway.app import app


class TestServer(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_sanity(self):
        resp = self.app.get('/echo?word=hello')
        self.assertTrue(b'hello' in resp.data)

    def test_available_models(self):
        resp = self.app.get('/available-models')
        self.assertTrue(b'HemlockRandomForestClassifier' in resp.data)
