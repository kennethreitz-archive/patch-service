# -*- coding: utf-8 -*-

"""
springcreek.models
~~~~~~~~~~~~~~~~~~

This module contains the database mdoels of SpringCreek.
"""

from datetime import datetime

from flask import url_for
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class BaseModel(object):
    created = db.Column(db.DateTime(timezone=False), default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        return db.session.commit()


# class BuildRequest(db.Model, BaseModel):
#     id = db.Column(db.Integer, primary_key=True)
#     buildpack_url = db.Column(db.String(300), unique=False)
#     application_url = db.Column(db.String(300), unique=False)
#     keep = db.Column(db.Boolean)

#     def __repr__(self):
#         return '<BuildRequest %r>' % self.id

#     @property
#     def result(self):
#         b_result = BuildResult.query.filter_by(request_id=self.id).first()

#         if not b_result:
#             b_result = BuildResult(request_id=self.id)
#             b_result.save()

#         return b_result

#     def __init__(self, buildpack_url, application_url, keep=False):
#         self.buildpack_url = buildpack_url
#         self.application_url = application_url
#         self.keep = keep

#     @property
#     def url(self):
#         return url_for('view_build', id=self.id)

# class BuildResult(db.Model, BaseModel):
#     id = db.Column(db.Integer, primary_key=True)
#     request_id = db.Column(db.Integer, db.ForeignKey(BuildRequest.id))
#     request = relationship(BuildRequest, uselist=False)
#     heroku_app = db.Column(db.String(50), unique=False)
#     install_log = db.Column(db.Text(), unique=False, nullable=True)
#     runtime_log = db.Column(db.Text(), unique=False, nullable=True)
#     success = db.Column(db.Boolean, nullable=True)
#     active = db.Column(db.Boolean, nullable=True)

#     def __init__(self, request_id):
#         self.request_id = request_id

#     def __repr__(self):
#         return '<BuildResult %r>' % self.id

#     @property
#     def heroku_url(self):
#         return 'http://{self.heroku_app}.herokuapp.com'.format(self=self)

#     @property
#     def git_url(self):
#         return 'git@heroku.com:{self.heroku_app}.git'.format(self=self)
