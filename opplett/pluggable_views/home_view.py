import os
import bcrypt

from flask import render_template, session
from flask.views import View

class HomeView(View):
    """View for the home-page-components page"""

    methods = ['GET']

    def dispatch_request(self):
        email = session.get('credentials', {}).get('id_token', {}).get('email', 'anonymous')
        context = {
            'authenticated_status': False if not session.get('invalid', True) else True,
            'authenticated_email': email,
            'authenticated_token': bcrypt.kdf(email.encode('utf-8'),
                                              salt=bytes('{}'.format(os.environ.get('SECRET_KEY')).encode()),
                                              rounds=50,
                                              desired_key_bytes=25
                                              )
        }
        return render_template('index.html', **context)