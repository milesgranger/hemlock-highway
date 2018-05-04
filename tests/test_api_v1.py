# -*- coding: utf-8 -*-

import unittest
import json
import moto
from hemlock_highway.server import app


class APIv1TestCase(unittest.TestCase):
    """
    Test expected functionality of the v1 web API
    """
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_sanity(self):
        resp = self.app.get('/echo?word=hello')
        self.assertTrue(b'hello' in resp.data)

    def test_available_models(self):
        resp = self.app.get('/api/v1/available-models')
        self.assertTrue(b'HemlockRandomForestClassifier' in resp.data)

    @moto.mock_s3
    def test_server_model_dump_load(self):
        """
        Perform the same test as above, only via the api
        """
        for config in [{'n_estimators': 123}, {}]:
            resp = self.app.post('/api/v1/dump-model', data={'model-name': 'HemlockRandomForestClassifier',
                                                             'model-config': json.dumps(config)})
            resp = json.loads(resp.data)
            self.assertTrue(resp.get('success'),
                            msg=f'Unexpected error after asking server to dump model: {resp}\nConfig: {config}'
                            )

    def test_dump_null_model(self):
        """
        Server should return no success if request to dump a null model
        """
        resp = self.app.post('/api/v1/dump-model', data={'model-name': None})
        resp_json = json.loads(resp.data)
        self.assertFalse(resp_json.get('success'))  # Can't successfully dump model if model name is None
        self.assertTrue(resp.status_code == 400)    # Status code should be 403, invalid request

    def test_dump_unknown_model(self):
        """
        Server should return no success if request to dump an unknown model
        """
        resp = self.app.post('/api/v1/dump-model', data={'model-name': 'this-model-does-not-exist'})
        resp_json = json.loads(resp.data)
        self.assertFalse(resp_json.get('success'))  # Can't successfully dump model if model name is unknown
        self.assertTrue(resp.status_code == 404)    # Status code should be 403, invalid request

    def test_fetch_model_parameters(self):
        """
        Ask for configurable model parameters
        """
        resp = self.app.get('/api/v1/model-parameters?model-name=HemlockRandomForestClassifier')
        data = json.loads(resp.data)
        self.assertTrue('n_estimators' in data.get('parameters'))

if __name__ == '__main__':
    unittest.main()
