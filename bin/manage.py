#!/usr/bin/env python
# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import sys, traceback
sys.path.insert(0, '.')

from flask.ext.script import Manager, Shell, Server
from flask.ext.dbshell import DbShell
from flask.ext.migrate import Migrate, MigrateCommand
import alembic, alembic.config

from Gthnk import create_app, db, security
app = create_app()

def _make_context():
    return dict(app=app, db=db, user_datastore=security.datastore)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("runserver", Server(port=app.config['PORT']))
manager.add_command("publicserver", Server(port=app.config['PORT'], host="0.0.0.0"))
manager.add_command('db', MigrateCommand)

@manager.option('-e', '--email', help='email address')
@manager.option('-p', '--password', help='password')
def create_user(email, password):
    "add a user to the database"
    from Gthnk import Models
    Models.User.create(email=email, password=password)

@manager.command
def init_db():
    "drop all databases, instantiate schemas"
    db.drop_all()
    db.create_all()
    db.session.commit()
    cfg = alembic.config.Config("migrations/alembic.ini")
    alembic.command.stamp(cfg, "head")

@manager.command
def populate_db():
    "insert a default set of objects"
    from flask.ext.diamond.utils import add_system_users
    add_system_users(security)

    #import Gthnk.importing as importing
    #importing.typical_workflow()

if __name__ == "__main__":
    try:
        manager.run()
    except Exception, e:
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
        print "Error: %s" % e
        print "Line: %d" % sys.exc_traceback.tb_lineno
