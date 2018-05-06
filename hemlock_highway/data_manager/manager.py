# -*- coding: utf-8 -*-

import csv
import io
import sys
import warnings

import boto3
import chardet
import requests

import pandas as pd

from hemlock_highway.settings import PROJECT_CONFIG


class DataManager:
    """
    DataManager is designed to be the interface between loading data form s3 or other endpoint
    into memory (either partially or fully)

    It is configurable so that the client can dictate a number of parameters in order to load the data.
    """

    X, y = pd.DataFrame(), pd.Series()

    def __new__(cls, *args, **kwargs):
        cls.s3_client = boto3.client('s3', region_name=PROJECT_CONFIG.AWS_REGION)
        return super().__new__(cls)

    def __init__(self, data_endpoint: str, target_column: str, **read_args):
        """
        Load the head of data stored at either a bucket location, or an http endpoint

        Parameters
        ----------
        data_endpoint: str  - Either an s3 bucket or an http endpoint
        target_column: str  - After loading the dataset, this is designated as the target column
        read_args: dict     - Any additional pandas.read_csv() kwargs
        """

        self.data_endpoint = data_endpoint
        self.target_column = target_column
        self.read_args = read_args

    def __getstate__(self):
        """Heading into a pickle, drop any loaded data"""
        if self._loaded:
            warnings.warn(message='Dropping X and y data; expecting to be pickled.', category=UserWarning)
            self.X, self.y = pd.DataFrame(), pd.Series()
        return self.__dict__

    @classmethod
    def generate_presigned_s3_url(cls, bucket: str, key: str, action='PUT') -> str:
        """
        Generate a presigned url to upload a dataset to
        """

        # Ensure we generate either get or post request url
        action = 'PUT' if action.upper() == 'POST' else action.upper()  # convert a 'POST' to 'PUT'
        if action not in ['PUT', 'GET']:
            raise ValueError(f'Can only generate a url for one of: "GET", "PUT"')

        # Generate the presigned url
        url = cls.s3_client.generate_presigned_url(
            'put_object' if action == 'PUT' else 'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3600,
            HttpMethod='PUT' if action == 'PUT' else 'GET'
        )
        return url

    @classmethod
    def list_s3_datasets(cls, bucket: str, dir: str) -> list:
        """
        List objects in a specific bucket and directory

        Returns
        -------
        List of dictionaries with keys of 'key' and 'size_bytes'
        """
        s3_client = boto3.client('s3', region_name=PROJECT_CONFIG.AWS_REGION)
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            MaxKeys=1000,
            Prefix=dir
        )
        return [{'key': v['Key'], 'size_bytes': v['Size']} for v in response['Contents']]

    @staticmethod
    def detect_encoding(data: bytes) -> str:
        """Given a byte string, return expected encoding"""
        return chardet.detect(data).get('encoding', 'iso-8859-1')

    def load(self, n_bytes=None):
        """
        Execute the load from either http or s3
        """

        # Load from http
        if any([self.data_endpoint.startswith(protocol) for protocol in ('http://', 'https://', 'tcp://')]):
            data = self._load_from_http(n_bytes=n_bytes)

        # Otherwise, assumed to be s3 bucket
        else:
            data = self._load_from_s3(n_bytes=n_bytes)

        data.seek(0)

        # Attempt to detect encoding or use existing encoding
        if 'encoding' not in self.read_args:
            encoding = self.detect_encoding(data.read(20000))
            self.read_args['encoding'] = self.read_args.get('encoding', encoding)
            data.seek(0)

        # Assign sniffed attributes of data to read_args if they haven't been assigned already by client.
        # skipping "lineterminator" since that gives back '\r\n' and pandas doesn't like that.
        dialect = csv.Sniffer().sniff(data.read(20000).decode(self.read_args['encoding']))
        data.seek(0)
        for attribute in filter(lambda attr: not attr.startswith('_') and attr not in ['lineterminator'], dir(dialect)):
            self.read_args[attribute] = self.read_args.get(attribute, getattr(dialect, attribute))

        # Actually load data into pandas
        self.X = pd.read_csv(filepath_or_buffer=data, **self.read_args)

        # Separate X and y
        self.y = self.X[self.target_column]
        self.X = self.X[[col for col in self.X.columns if col != self.target_column]]

    def _load_from_http(self, n_bytes: int=None) -> io.BytesIO:
        # Stream from source writing by chunk size of 1mb or n_bytes
        # if n_bytes is defined, load that and break after one iteration.
        data = io.BytesIO()
        resp = requests.get(self.data_endpoint, stream=True)
        if resp.ok:
            for chunk in resp.iter_content():
                if chunk:
                    data.write(chunk)
                if n_bytes and sys.getsizeof(data) >= n_bytes:
                    break
            return data
        else:
            raise IOError(
                f'Unable to get data from: {self.data_endpoint}; Got: {resp.status_code} Content: {resp.content}'
            )

    def _load_from_s3(self, n_bytes: int=None) -> io.BytesIO:
        # Request the object
        resp = self.s3_client.get_object(Bucket=self.data_endpoint.split('/')[0],
                                         Key='/'.join(self.data_endpoint.split('/')[1:]),
                                         Range=f'bytes=0-{n_bytes or ""}'
                                         )

        # Read object if request was successful or raise an error
        if str(resp['ResponseMetadata']['HTTPStatusCode']).startswith('20'):
            data = io.BytesIO(resp['Body'].read())
            return data
        else:
            raise IOError(f'Error fetching dataset from S3: {resp}')

    @property
    def _loaded(self):
        return self.X.shape[0] > 0 if hasattr(self.X, 'shape') else False
