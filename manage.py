#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flaskext.script import Manager
from flask.ext.celery import install_commands as install_celery

from springcreek import app
from springcreek.core import db, heroku


manager = Manager(app)
install_celery(manager)

@manager.command
def syncdb():
    """Initializes the database."""
    db.create_all()

@manager.command
def destroy_all_software():

    for i, app in enumerate(heroku.apps):

        if i != 0:
            app.destroy()
            print 'destroyed {0}'.format(app.name)



if __name__ == "__main__":
    manager.run()