import os
import bcrypt

from datetime import datetime
from flask import render_template
from flask.views import View

class HomeView(View):
    """View for the home-page-components page"""

    methods = ['GET']

    def dispatch_request(self):
        context = {
            'authenticated_status': True,
            'authenticated_user': 'milesg',
            'authenticated_token': bcrypt.kdf(b'milesg',
                                              salt=bytes('{}{}'.format(os.environ.get('SECRET_KEY'),
                                                                       datetime.now().day).encode()),
                                              rounds=50,
                                              desired_key_bytes=25
                                              )
        }
        return render_template('index.html', **context)