# -*- coding: utf-8 -*-

import json
import unittest
import responses
from hemlock_highway.data_manager import DataManager
from hemlock_highway.model_runner import app
from hemlock_highway.ml.models import HemlockRandomForestClassifier
import moto


class ModelRunnerTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    @moto.mock_s3
    def test_load_model(self):
        """
        Test that a dumped model can be loaded from ModelRunner server
        """
        responses.add_passthru('https://')
        clf = HemlockRandomForestClassifier()
        clf.data_manager = DataManager(
            data_endpoint='https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv',
            target_column='species'
        )
        clf.dump(bucket='test', key='models/test-model.pkl')
        resp = self.app.post('/train-model', data={'model-location': 'test/models/test-model.pkl'})
        data = json.loads(resp.data)
        self.assertTrue(data.get('success'))
