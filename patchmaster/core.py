# -*- coding: utf-8 -*-

"""
springcreek.core
~~~~~~~~~~~~~~~~

This module contains the main application of SpringCreek.
"""

import os
import tempfile
from datetime import datetime, timedelta

import heroku
import envoy
from flask import Flask, render_template, request, redirect, url_for, Response
from flask.views import MethodView

from flask_debugtoolbar import DebugToolbarExtension
from flask_heroku import Heroku
from flask_googlefed import GoogleAuth
from raven.contrib.flask import Sentry
from flask.ext.celery import Celery
from sqlalchemy import desc

from .models import db, BuildRequest, BuildResult
from .hacks import ContextTask, setup_ssh_keys, gen_lines


app = Flask(__name__)

# Don't ask.
setup_ssh_keys()

app.secret_key = 'some-secret-key'

# Use gevent workers for celery.
app.config['CELERYD_POOL'] = 'eventlet'
app.config['CELERYD_CONCURRENCY'] = 1000


# Heroku API Key.
app.config['HEROKU_API_KEY'] = os.environ.get('HEROKU_API_KEY')
app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Bootstrap Heroku environment variables.
heroku_env = Heroku(app)

# Intialize databse configuration.
db.init_app(app)

sentry = Sentry(app)
auth = GoogleAuth(app)
toolbar = DebugToolbarExtension(app)
celery = Celery(app)

heroku = heroku.from_key(app.config['HEROKU_API_KEY'] )


@celery.task(base=ContextTask)
def build_task(request_id, tail=False):

    request = BuildRequest.query.filter_by(id=request_id).first()
    result = request.result

    app.logger.info('Starting build for {0}.'.format(request))

    # Replace # w/ @
    _split_url = request.application_url.split('#')
    clone_url = _split_url[0]
    clone_ref = _split_url[1] if len(_split_url) > 1 else 'HEAD'


    h_app = heroku.apps.add(stack='cedar')
    h_app.config['BUILDPACK_URL'] = request.buildpack_url
    result.heroku_app = h_app.name
    result.save()

    app.logger.info('Heroku app {0} created for {1}.'.format(h_app, request))

    pwd = tempfile.mkdtemp(prefix='springcreek')
    app.logger.info('Temp dir {0} created for {1}.'.format(pwd, request))
    os.chdir(pwd)

    app.logger.info('Cloning {0} created for {1}.'.format(clone_url, request))
    envoy.run('git clone {0} repo'.format(clone_url))
    os.chdir('repo')

    app.logger.info('Pushing app to {0} for {1}.'.format(h_app, request))

    git_push = r'git push {result.git_url} {ref}:master'.format(result=result, ref=clone_ref)
    app.logger.info(git_push)

    if tail:
        c = envoy.connect(git_push)
        return c

    c = envoy.run(git_push)
    app.logger.info('Push exit code: {c.status_code}'.format(c=c))

    result.success = (c.status_code == 0)
    result.install_log = c.std_err
    result.active = True
    result.save()

    if not request.keep:
        later = datetime.now() + timedelta(hours=2)
        destroy_app.apply_async(args=[request_id], eta=later)


@celery.task(base=ContextTask)
def destroy_app(request_id):

    request = BuildRequest.query.filter_by(id=request_id).first()
    result = request.result

    app.logger.info('Destroying app {0}.'.format(result.heroku_app))

    # Destroy the app.
    h_app = heroku.apps[result.heroku_app]
    h_app.destroy()

    result.active = False
    result.save()



@app.route('/')
@auth.required
def landing_page():
    return render_template('index.html')

class Builds(MethodView):

    @auth.required
    def get(self):
        builds = BuildRequest.query.order_by(desc(BuildRequest.created)).all()
        return render_template('builds.html', builds=builds)

    @auth.required
    def post(self):
        """Create a new BuildRequest."""

        r = BuildRequest(
            buildpack_url=request.form.get('buildpack_url'),
            application_url=request.form.get('application_url'),
            keep=('keep' in request.form)
        )
        db.session.add(r)
        db.session.commit()

        if request.args.get('tail'):
            c = build_task(r.id, tail=True)
            return Response(gen_lines(c))

        else:

            # Send the build task off to work.
            build_task.delay(r.id, tail=False)
            return redirect(r.url)

app.add_url_rule('/builds', view_func=Builds.as_view('builds'))

@app.route('/builds/<id>')
@auth.required
def view_build(id):
    b_request = BuildRequest.query.filter_by(id=id).first()

    context = dict(
        request=b_request
    )

    if b_request:
        return render_template('build.html', **context)
    else:
        return redirect(url_for('builds'))


if __name__ == '__main__':
    app.run()