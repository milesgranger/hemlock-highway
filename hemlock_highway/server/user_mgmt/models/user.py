# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin


__all__ = [
    'db',
    'User',
    'MachineLearningModel',
    'Transaction',
    'OAuth'
]

db = SQLAlchemy()


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email       = db.Column(db.String(256), unique=True)
    name_first  = db.Column(db.String(256), unique=False, nullable=True)
    name_last   = db.Column(db.String(256), unique=False, nullable=True)

    models      = db.relationship('MachineLearningModel', back_populates='user')
    transactions= db.relationship('Transaction', back_populates='user')


class MachineLearningModel(db.Model):

    __tablename__ = 'ml_model'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id     = db.Column(db.Integer, db.ForeignKey(User.id))
    name        = db.Column(db.String(256), unique=False)
    trained     = db.Column(db.Boolean, default=False)
    size_bytes  = db.Column(db.Integer)

    user        = db.relationship(User, back_populates='models')

    def serialize(self):
        return {
            'name': self.name,
            'trained': self.trained,
            'size': self.size_bytes
        }


class Transaction(db.Model):

    __tablename__ = 'transaction'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id     = db.Column(db.Integer, db.ForeignKey(User.id))
    amount      = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)

    user        = db.relationship(User, back_populates='transactions')


class OAuth(OAuthConsumerMixin, db.Model):

    __tablename__ = 'oauth'

    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

