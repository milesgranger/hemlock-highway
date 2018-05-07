# -*- coding: utf-8 -*-

import abc
import boto3
import zlib
import pickle

from hemlock_highway.settings import PROJECT_CONFIG
from hemlock_highway.data_manager import DataManager


class HemlockModelBase:

    # Each model should have a DataManager to manage the handling of the IO/parsing of data for the model.
    data_manager = DataManager('', '')

    def __new__(cls, *args, **kwargs):
        cls.s3_client = boto3.client('s3', region_name=PROJECT_CONFIG.AWS_REGION)
        return super().__new__(cls)

    @staticmethod
    @abc.abstractstaticmethod
    def configurable_parameters():
        """
        Return a mapping of parameter names and submapping of type and valid values
        ie. {
            'n_estimators': {'type': int, 'range': }
        }
        """
        ...

    @abc.abstractmethod
    def dump(self, bucket: str, key: str):
        """
        Dump a model to s3
        """
        model_out = zlib.compress(pickle.dumps(self))
        self.s3_client.create_bucket(Bucket=bucket)
        resp = self.s3_client.put_object(Bucket=bucket, Key=key, Body=model_out)
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            raise IOError(f'Unable to serialize model to S3 location: {bucket}/{key}\nBoto3 response: {resp}')

    @classmethod
    @abc.abstractmethod
    def load(cls, bucket: str, key: str):
        """
        Load a model from S3
        """
        model = cls().s3_client.get_object(Bucket=bucket, Key=f'{key}')['Body'].read()
        model = pickle.loads(zlib.decompress(model))
        return model


__all__ = [
    'HemlockModelBase'
]
