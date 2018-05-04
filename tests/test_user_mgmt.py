# -*- coding: utf-8 -*-

import unittest
from hemlock_highway.server import app
from tests.utils import fake_google_authenticated_user


class UserMgmtTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    @fake_google_authenticated_user(username='test-user')
    def test_google_login(self):
        """
        Test an authenticated user trying to login
        """
        response = self.app.get('/login-google')
        self.assertTrue(
            b'test-user' in response.data, msg=f'Expected response to have "test-user", found {response.data}'
        )


if __name__ == '__main__':
    unittest.main()
