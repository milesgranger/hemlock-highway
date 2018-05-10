# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email       = db.Column(db.String(256), unique=True)
    name_first  = db.Column(db.String(256), unique=False, nullable=True)
    name_last   = db.Column(db.String(256), unique=False, nullable=True)
    transaction = db.relationship('Transaction')
    model       = db.relationship('MachineLearningModel')


class MachineLearningModel(db.Model):

    __tablename__ = 'ml_model'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id     = db.Column(db.Integer, db.ForeignKey(User.id))
    name        = db.Column(db.String(256), unique=False)
    trained     = db.Column(db.Boolean, default=False)
    size_bytes  = db.Column(db.Integer)


class Transaction(db.Model):

    __tablename__ = 'transaction'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id     = db.Column(db.Integer, db.ForeignKey(User.id))
    amount      = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)


class OAuth(OAuthConsumerMixin, db.Model):

    __tablename__ = 'oauth'

    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

