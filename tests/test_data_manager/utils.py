# -*- coding: utf-8 -*-

import os
import boto3
import moto
from contextlib import contextmanager
from hemlock_highway.settings import PROJECT_CONFIG


@contextmanager
def fake_data_on_s3(local_dataset, bucket, key):

    with moto.mock_s3():
        s3 = boto3.client('s3', region_name=PROJECT_CONFIG.AWS_REGION)
        s3.create_bucket(Bucket=bucket)
        with open(os.path.join(PROJECT_CONFIG.TEST_DATA_DIR, local_dataset), 'rb') as f:
            s3.put_object(Bucket=bucket, Key=key, Body=f.read())

        yield
