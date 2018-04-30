# -*- coding: utf-8 -*-

import unittest
import moto
import boto3


class HemlockModelsTestCase(unittest.TestCase):
    """
    Test the functionality of implemented models, outside of the web API
    """
    def setUp(self):
        pass

    @moto.mock_s3
    def test_dump_n_load_model(self):
        """
        Test the model can be dumped to s3 and loaded back
        TODO: Test all models
        """
        from hemlock_highway.models import HemlockRandomForestClassifier
        client = boto3.client('s3', region_name='us-east-1')

        clf1 = HemlockRandomForestClassifier()
        clf1.dump(s3_client=client, bucket='hemlock-highway-test', key='tests', name='model.pkl')

        clf2 = HemlockRandomForestClassifier.load(s3_client=client, bucket='hemlock-highway-test', key='tests', name='model.pkl')

        self.assertTrue(isinstance(clf2, HemlockRandomForestClassifier),
                        msg=f'Expected loaded model from s3 to be instand of HemlockRandomForestClassifier, instead ' \
                            f'got {type(clf2)}'
                        )


if __name__ == '__main__':
    unittest.main()
