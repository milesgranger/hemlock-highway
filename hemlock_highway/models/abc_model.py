# -*- coding: utf-8 -*-

import abc
import boto3
import zlib
import pickle


class AbcHemlockModel:

    client = boto3.client('s3', region_name='us-east-1')

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
    def dump(self, bucket: str, key: str, name: str):
        """
        Dump a model to s3
        """
        model_out = zlib.compress(pickle.dumps(self))
        self.client.create_bucket(Bucket=bucket)
        resp = self.client.put_object(Bucket=bucket, Key=f'{key}/{name}', Body=model_out)
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            raise IOError(f'Unable to serialize model to S3 location: {bucket}/{key}/{name}\nBoto3 response: {resp}')

    @classmethod
    @abc.abstractmethod
    def load(cls, bucket: str, key: str, name: str):
        """
        Load a model from S3
        """
        model = cls.client.get_object(Bucket=bucket, Key=f'{key}/{name}')['Body'].read()
        model = pickle.loads(zlib.decompress(model))
        return model


__all__ = [
    'AbcHemlockModel'
]
