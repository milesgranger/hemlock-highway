# -*- coding: utf-8 -*-

from unittest import mock
from contextlib import contextmanager
from flask_dance.consumer.requests import OAuth2Session
from requests.models import Response


@contextmanager
def fake_google_authenticated_user(username):
    """
    Fake a login of an authenticated user
    """
    with mock.patch.object(OAuth2Session, 'authorized') as _google, \
            mock.patch.object(Response, 'ok') as resp, \
            mock.patch.object(Response, 'json') as resp:

        # Make google return authorized
        type(_google).authorized = mock.PropertyMock(return_value=True)

        # Make response return Ok and the requested username
        type(resp).ok = mock.PropertyMock(return_value=True)
        resp.return_value = {'name': username}
        yield



