import s3fs
import os
import json
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

    # Ensure user is validated first; otherwise return to OAuth login
    try:
        if not google.authorized:
            return redirect(url_for('google.login'))
        resp = google.get('/oauth2/v2/userinfo')
        # Get google info about user
        user = User(resp.json(), source='google')
        return user
    except:
        return redirect(url_for('google.login'))



def list_files(username, path=''):
    """
    Given username and option path, return file details
    """
    fs = s3fs.S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'),
                           secret=os.environ.get('AWS_SECRET_ACCESS_KEY')
                           )
    files = fs.ls('{bucket}/{username}/{path}'.format(bucket=os.environ.get('S3_BUCKET'),
                                                      username=username,
                                                      path=path),
                  detail=True)

    for file in files:
        # Forget about the first two, which is ${S3_BUCKET}/${username}/path/to/file
        file['Key'] = '/'.join(file['Key'].split('/')[2:])
    return files
