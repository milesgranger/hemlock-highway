# -*- coding: utf-8 -*-

import io
import boto3
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

    def load(self):
        """
        Execute the load from either http or s3
        """
        if self.data_endpoint.startswith('http://') or self.data_endpoint.startswith('https://'):
            self.X = pd.read_csv(filepath_or_buffer=self.data_endpoint, **self.read_args)
        else:
            resp = self.s3_client.get_object(Bucket=self.data_endpoint.split('/')[0],
                                             Key='/'.join(self.data_endpoint.split('/')[1:])
                                             )
            if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
                self.X = pd.read_csv(io.BytesIO(resp['Body'].read()), **self.read_args)
            else:
                raise IOError(f'Error fetching dataset from S3: {resp}')

        self.y = self.X[self.target_column]
        self.X = self.X[[col for col in self.X.columns if col != self.target_column]]

    @property
    def _loaded(self):
        return self.X.shape[0] > 0 if hasattr(self.X, 'shape') else False
