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


def get_s3fs():
    """
    Convenience method, Return connected s3fs object
    """
    fs = s3fs.S3FileSystem(key=os.environ.get('AWS_ACCESS_KEY_ID'),
                           secret=os.environ.get('AWS_SECRET_ACCESS_KEY')
                           )
    return fs


def list_files_and_folders(username, path=''):
    """
    Given username and option path, return file details
    """
    fs = get_s3fs()
    files = fs.ls('{bucket}/{username}/{path}'.format(bucket=os.environ.get('S3_BUCKET'),
                                                      username=username,
                                                      path=path),
                  detail=True)
    for file in files:
        file['Key'] = os.path.basename(file['Key'])

    folders_tmp = sorted([f for f in files if not f.get('Size') or f.get('StoargeClass') == 'DIRECTORY'],
                         key=lambda d: d.get('StorageClass'),
                         reverse=False)

    # Folders are listed twice, once as a directory, another as a file with Size of 0
    last_key, folders = None, []
    for folder in folders_tmp:
        if folder.get('Key') == last_key:
            continue
        else:
            folders.append(folder)
            last_key = folder.get('Key')

    files = sorted([file for file in files if file.get('Size')], key=lambda dic: dic.get('Size'))
    return folders, files
