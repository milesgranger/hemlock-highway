# -*- coding: utf-8 -*-

import os
import sys
import unittest
import moto

import botocore.exceptions
from .utils import fake_data_on_s3


class DataManagerTestCase(unittest.TestCase):

    def setUp(self):

        # Test data directory
        self.DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

    @fake_data_on_s3(local_dataset='iris.csv', bucket='test', key='data/basic.csv')
    def test_load_from_s3(self):
        """
        Test the basic loading of a dataset.
        """
        from hemlock_highway.data_manager import DataManager
        dm = DataManager(data_endpoint='test/data/basic.csv', target_column='species')
        self.assertFalse(dm._loaded, msg='DataManger should not load data on initialization! Reports it is loaded!')
        dm.load()
        self.assertTrue(dm._loaded, msg='After asking to load data, DataManager is reporting it is not loaded!')
        self.assertTrue(dm.X.shape[0] > 0, msg='DataManager reports it is loaded, but does not have any data in X!')

    @moto.mock_s3
    def test_load_non_existant_data(self):
        """
        Test IOError when trying to load a non-existant dataset.
        """
        from hemlock_highway.data_manager import DataManager
        dm = DataManager(data_endpoint='test/data/basic.csv', target_column='species')

        # Should raise an exception when trying to load a dataset that doesn't exist.
        with self.assertRaises(botocore.exceptions.ClientError):
            dm.load()

    def test_load_from_http(self):
        """
        Ensure dataloader can load a dataset via http
        """
        from hemlock_highway.data_manager import DataManager
        dm = DataManager(
            data_endpoint='https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv',
            target_column='species'
        )
        dm.load()
        self.assertTrue('petal_length' in dm.X.columns,
                        msg=f'Expected "petal_length" to be in X, but found {dm.X.columns}')

    @fake_data_on_s3(local_dataset='iris.csv', bucket='test', key='data/basic.csv')
    def test_load_first_mb_s3(self):
        """
        Ensure dataloader can load just the for n_bytes from s3
        """
        from hemlock_highway.data_manager import DataManager
        dm = DataManager(data_endpoint='test/data/basic.csv', target_column='species')
        dm.load(n_bytes=1024)
        size = sys.getsizeof(dm.X)
        self.assertLess(size, 1512, msg=f'Size of data is > 1.5mb; it is {size} bytes')

    def test_load_first_mb_http(self):
        """
        Ensure dataloader can load just the for n_bytes from s3
        """
        from hemlock_highway.data_manager import DataManager
        dm = DataManager(
            data_endpoint='https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv',
            target_column='species'
        )
        dm.load(n_bytes=1024)
        size = sys.getsizeof(dm.X)
        self.assertLess(size, 1512, msg=f'Size of data is > 1.5mb; it is {size} bytes')


if __name__ == '__main__':
    unittest.main()
