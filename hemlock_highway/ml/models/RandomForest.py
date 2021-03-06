# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from hemlock_highway.ml.models import HemlockModelBase


class HemlockRandomForestClassifier(RandomForestClassifier, HemlockModelBase):

    @staticmethod
    def configurable_parameters():
        return {
            'bootstrap': {
                'type': 'boolean',
                'options': [True, False]
            },
            'class_weight': {
                'type': 'string',
                'options': ('balanced', None)
            },
            'n_estimators': {
                'type': 'integer',
                'options': list(range(1, 100))
            }
        }


__all__ = [
    'HemlockRandomForestClassifier'
]
