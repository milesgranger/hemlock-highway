# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email       = db.Column(db.String(256), unique=True)
    name_first  = db.Column(db.String(256), unique=False, nullable=True)
    name_last   = db.Column(db.String(256), unique=False, nullable=True)






class OAuth(OAuthConsumerMixin, db.Model):

    __tablename__ = 'oauth'

    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

