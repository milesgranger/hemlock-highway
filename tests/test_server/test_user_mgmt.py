# -*- coding: utf-8 -*-

import unittest
from hemlock_highway.server import app
from tests.test_server.utils import fake_google_authenticated_user


class UserMgmtTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_unauthenticated_dashboard(self):
        """
        Test an unauthenticated user attempting to access dashboard
        """
        response = self.app.get('/dashboard')
        self.assertTrue(
            b'Unauthorized' in response.data, msg=f'Expected unauthorized'
        )


if __name__ == '__main__':
    unittest.main()
