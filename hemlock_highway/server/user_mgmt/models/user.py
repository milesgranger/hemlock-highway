# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import google
from flask_login import UserMixin


db = SQLAlchemy()


class UserProto(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    picture = db.Column(db.String(1000), nullable=True)
    gender = db.Column(db.String(1), nullable=True)
    locale = db.Column(db.String(10), nullable=True)

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

