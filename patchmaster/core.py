# -*- coding: utf-8 -*-

"""
springcreek.core
~~~~~~~~~~~~~~~~

This module contains the main application of SpringCreek.
"""

import os
import tempfile
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, Response
from flask.views import MethodView

from flask_heroku import Heroku
from raven.contrib.flask import Sentry
from flask.ext.celery import Celery
from sqlalchemy import desc

from .models import db

app = Flask(__name__)

app.secret_key = 'some-secret-key'

# Use gevent workers for celery.
app.config['CELERYD_POOL'] = 'gevent'
app.config['CELERYD_CONCURRENCY'] = 1000

# Bootstrap Heroku environment variables.
heroku_env = Heroku(app)

# Intialize databse configuration.
db.init_app(app)

sentry = Sentry(app)
celery = Celery(app)



@app.route('/')
def landing_page():
    return 'hi'

# class Builds(MethodView):

#     @auth.required
#     def get(self):
#         builds = BuildRequest.query.order_by(desc(BuildRequest.created)).all()
#         return render_template('builds.html', builds=builds)

#     @auth.required
#     def post(self):
#         """Create a new BuildRequest."""

#         r = BuildRequest(
#             buildpack_url=request.form.get('buildpack_url'),
#             application_url=request.form.get('application_url'),
#             keep=('keep' in request.form)
#         )
#         db.session.add(r)
#         db.session.commit()

#         if request.args.get('tail'):
#             c = build_task(r.id, tail=True)
#             return Response(gen_lines(c))

#         else:

#             # Send the build task off to work.
#             build_task.delay(r.id, tail=False)
#             return redirect(r.url)

# app.add_url_rule('/builds', view_func=Builds.as_view('builds'))


if __name__ == '__main__':
    app.run()