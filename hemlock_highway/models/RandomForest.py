# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from hemlock_highway.models import AbcHemlockModel


class HemlockRandomForestClassifier(RandomForestClassifier, AbcHemlockModel):

    @property
    def configurable_parameters(self):
        return {
            'bootstrap': {
                'type': bool,
                'options': [True, False]
            },
            'class_weight': {
                'type': str,
                'options': ('balanced', None)
            },
            'n_estimators': {
                'type': int,
                'options': tuple(range(1, 100))
            }
        }
