# -*- coding: utf-8 -*-

from hemlock_highway.ml import HemlockModelBase


class ModelRunner:
    """
    Responsible for running a model in either training/testing/prediction modes
    """

    def __init__(self, model: HemlockModelBase=None, bucket: str=None, key: str=None):
        """
        Load the model, but not the data using either directly passing model or pointing to s3 location
        """
        if model is None and all((m is None for m in (bucket, key))):
            raise ValueError('Must specify either a loaded model or an s3 location specifying both bucket and key!')

        self.model = model if model is not None else HemlockModelBase.load(bucket, key)

    def fit(self):
        """Fit the underlying model to the data from it's DataManager"""
        X, y = self.model.data_manager.load()
        self.model.fit(X, y)
        return True

    def predict(self):
        """Predict using model from DataManager data"""
        X, y = self.model.data_manager.load()
        return self.model.predict(X)
