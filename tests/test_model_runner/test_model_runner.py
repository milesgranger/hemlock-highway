# -*- coding: utf-8 -*-

import json
import unittest
import responses
import moto
from sklearn.exceptions import NotFittedError

from hemlock_highway.data_manager import DataManager
from hemlock_highway.model_runner import app, ModelRunner
from hemlock_highway.ml.models import HemlockRandomForestClassifier, HemlockModelBase

from tests.utils import fake_data_on_s3


class ModelRunnerTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    @moto.mock_s3
    def test_model_runner_loader(self):
        """
        Model dumped to s3, should be able to be instantiated through the ModelRunner class
        """
        # Test dumping model to s3 and then loading it back via ModelRunner
        clf1 = HemlockRandomForestClassifier()
        clf1.dump(bucket='test', key='mymodel.pkl')
        clf2 = ModelRunner(bucket='test', key='mymodel.pkl')
        self.assertIsInstance(clf2.model, HemlockModelBase)

        with self.assertRaises(ValueError):
            ModelRunner()  # Fail if not passing an existing model or an s3 location

        # Test passing model directly to ModelRunner
        clf2 = ModelRunner(model=clf1)
        self.assertIsInstance(clf2.model, HemlockModelBase)

    @fake_data_on_s3(local_dataset='iris.csv', bucket='test', key='iris.csv')
    def test_model_runner_process(self):
        """
        Test core process of loading data, fitting and making predictions using underlying model
        """
        # Define some model with it's data manager
        clf = HemlockRandomForestClassifier()
        clf.data_manager = DataManager(data_endpoint='test/iris.csv', target_column='species')
        clf.data_manager.load()

        # Pass model to ModelRunner
        runner = ModelRunner(clf)

        # Model isn't fitted, so it shouldn't be able to predict anything
        with self.assertRaises(NotFittedError, msg="Model isn't fitted, so it shouldn't be able to predict anything!"):
            runner.predict()

        # Fit & predict, ensuring that the orignal, runner, and predicted data sizes match
        runner.fit()
        data = runner.predict()
        original_size = clf.data_manager.X.shape[0]
        runner_size = runner.model.data_manager.X.shape[0]
        predicted_size = data.shape[0]
        self.assertTrue(
            original_size == runner_size == predicted_size,
            f'Expected: '
            f' original data ({original_size}) == runner data ({runner_size}) == predicted data ({predicted_size})'
        )

    @moto.mock_s3
    def test_load_model(self):
        """
        Test that a dumped model can be loaded from ModelRunner server
        """
        responses.add_passthru('https://')  # mock_s3 breaks requests
        clf = HemlockRandomForestClassifier()
        clf.data_manager = DataManager(
            data_endpoint='https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv',
            target_column='species'
        )
        clf.dump(bucket='test', key='models/test-model.pkl')
        resp = self.app.post('/train-model', data={'model-location': 'test/models/test-model.pkl'})
        data = json.loads(resp.data)
        self.assertTrue(data.get('success'))
