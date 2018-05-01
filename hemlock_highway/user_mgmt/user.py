# -*- coding: utf-8 -*-

from flask_dance.contrib.google import google


class User:

    name = None
    picture = None
    gender = None
    locale = None

    def __init__(self, name, picture, gender, locale):
        self.name = name
        self.picture = picture
        self.gender = gender
        self.locale = locale

    @classmethod
    def from_flask_dance_session(cls, session_caller):
        """
        Return an instance of user from a caller resulting from authenticated flask_dance
        ie. flask_dance.contrib.google.google
        """
        if session_caller == google:
            return cls._from_google(session_caller)
        else:
            raise NotImplementedError(f'Can not make User from unknown session_caller: {session_caller}')

    @classmethod
    def _from_google(cls, caller):
        """From a google caller"""
        resp = caller.get('/oauth2/v1/userinfo?alt=json')
        if not resp.ok:
            raise IOError(f'Unable to get user data from Google: {resp.content}')
        resp = resp.json()
        return cls(name=resp.get('name') or resp.get('given_name'),
                   picture=resp.get('picture'),
                   gender=resp.get('gender'),
                   locale=resp.get('locale')
                   )
