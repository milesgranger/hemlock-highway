# -*- coding: utf-8 -*-

import io
import sys
import boto3
import requests
import pandas as pd
from hemlock_highway.settings import PROJECT_CONFIG


class DataManager:

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

    def load(self, n_bytes=None):
        """
        Execute the load from either http or s3
        TODO: Implement loading of n_bytes
        """

        data = io.BytesIO()  # Holder the raw bytes either from s3 or some http endpoint.

        # Load from http
        if any([self.data_endpoint.startswith(protocol) for protocol in ('http://', 'https://', 'tcp://')]):

            # Stream from source writing by chunk size of 1mb or n_bytes
            # if n_bytes is defined, load that and break after one iteration.
            resp = requests.get(self.data_endpoint, stream=True)
            if resp.ok:
                for chunk in resp.iter_content():
                    if chunk:
                        data.write(chunk)
                    if n_bytes and sys.getsizeof(data) >= n_bytes:
                        break
            else:
                raise IOError(
                    f'Unable to get data from: {self.data_endpoint}; Got: {resp.status_code} Content: {resp.content}'
                )

        # Otherwise, assumed to be s3 bucket
        else:

            # Request the object
            resp = self.s3_client.get_object(Bucket=self.data_endpoint.split('/')[0],
                                             Key='/'.join(self.data_endpoint.split('/')[1:]),
                                             Range=f'bytes=0-{n_bytes or ""}'
                                             )

            # Read object if request was successful or raise an error
            if str(resp['ResponseMetadata']['HTTPStatusCode']).startswith('20'):
                data.write(resp['Body'].read())
            else:
                raise IOError(f'Error fetching dataset from S3: {resp}')

        # Seek the start of io object and read into pandas
        data.seek(0)

        # Separate X and y
        self.X = pd.read_csv(filepath_or_buffer=data, **self.read_args)
        self.y = self.X[self.target_column]
        self.X = self.X[[col for col in self.X.columns if col != self.target_column]]

    @property
    def _loaded(self):
        return self.X.shape[0] > 0 if hasattr(self.X, 'shape') else False
