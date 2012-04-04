# -*- coding: utf-8 -*-

"""
springcreek.models
~~~~~~~~~~~~~~~~~~

This module contains the database mdoels of SpringCreek.
"""

from uuid import uuid4
from datetime import datetime

from flask import url_for
from flaskext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_token():
    return uuid4().hex

class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        return db.session.commit()


class Account(db.Model, BaseModel):
    """A user's authentication account."""

    username = db.Column(db.String(40), unique=True, primary_key=True)
    token = db.Column(db.String(40), unique=True, primary_key=True, default=generate_token)
    password = db.Column(db.String(100), unique=False)
    sudo = db.Column(db.Boolean, default=False)

    def __init__(self, arg):
        super(Account, self).__init__()

class User(db.Model, BaseModel):
    """A User profile."""

    name = db.Column(db.String(40), unique=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, primary_key=True)
    bio = db.Column(db.String(10000))
    website = db.Column(db.String(300))
    location = db.Column(db.String(100))

    def __init__(self, arg):
        super(User, self).__init__()


class Patch(db.Model, BaseModel):
    """A User's patch."""

    name = db.Column(db.String(100), unique=True, primary_key=True)
    description = db.Column(db.String(10000))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    downloads = db.relationship('Download', backref='patch')

    bio = db.Column(db.String(2000))
    website = db.Column(db.String(300))
    location = db.Column(db.String(100))

    def __init__(self, arg):
        super(User, self).__init__()


class Download(db.Model, BaseModel):
    """A User's download."""
    __table__ = 'download'

    patch_id = db.Column(db.Integer, db.ForeignKey(Patch.id))
    checksum = db.Column(db.String(100))
    file_name = db.Column(db.String(100))
    file_size = db.Column(db.Integer)

    def __init__(self, arg):
        super(User, self).__init__()


class Device(db.Model, BaseModel):
    """A Patch Device."""

    name = db.Column(db.String(100))
    vanity_name = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    patches = db.relationship('Patch', backref='device')

    def __init__(self, arg):
        super(User, self).__init__()


class Category(db.Model, BaseModel):
    """A Patch category."""

    name = db.Column(db.String(100))
    vanity_name = db.Column(db.String(100))
    patches = db.relationship('Patch', backref='category')

    def __init__(self, arg):
        super(User, self).__init__()