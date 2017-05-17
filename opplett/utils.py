from flask import redirect, url_for
from flask_dance.contrib.google import google

class User:
    """
    Representation of an OAuth user
    Data is the json acquired from successful authentication via an OAuth service. Google, etc.
    """
    def __init__(self, data, source):
        if source == 'google':
            self.name = data.get('name')
            self.profile_img = data.get('picture')
            self.email = data.get('email')

def get_user_via_oauth():
    # Ensure user is validated first.
    try:
        if not google.authorized:
            return redirect(url_for('google.login'))
        resp = google.get('/oauth2/v2/userinfo')
    except:
        return redirect(url_for('google.login'))

    # Get google info about user
    user = User(resp.json(), source='google')
    return user