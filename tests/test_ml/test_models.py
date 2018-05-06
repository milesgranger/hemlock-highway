# -*- coding: utf-8 -*-

import unittest
import moto


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
        from hemlock_highway.ml.models import HemlockRandomForestClassifier

        clf1 = HemlockRandomForestClassifier()
        clf1.dump(bucket='hemlock-highway-test', key='tests/model.pkl')

        clf2 = HemlockRandomForestClassifier.load(bucket='hemlock-highway-test', key='tests/model.pkl')

        self.assertTrue(isinstance(clf2, HemlockRandomForestClassifier),
                        msg=f'Expected loaded model from s3 to be instand of HemlockRandomForestClassifier, instead ' \
                            f'got {type(clf2)}'
                        )

    def test_data_manager_property(self):
        """Even though it's an abstract property, it won't raise an error if the attribute doesn't exist
           like it does if the method isn't implemented.
        """
        from hemlock_highway.ml.models import HemlockRandomForestClassifier
        from hemlock_highway.data_manager import DataManager
        clf = HemlockRandomForestClassifier()
        self.assertTrue(hasattr(clf, 'data_manager'),
                        msg=f'{clf.__class__} has no attribute "data_manager", which should be instance of DataManager')
        self.assertTrue(isinstance(clf.data_manager, DataManager))


if __name__ == '__main__':
    unittest.main()
