# -*- coding: utf-8 -*-

import abc


class AbcHemlockModel:

    @property
    @abc.abstractmethod
    def parameters(self):
        """
        Return a mapping of parameter names and submapping of type and valid values
        ie. {
            'n_estimators': {'type': int, 'range': }
        }
        """
        ...
