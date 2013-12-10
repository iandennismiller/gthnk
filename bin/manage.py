#!/usr/bin/env python
# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import sys
sys.path.insert(0, '.')

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
import GTLibrary.models as Model
from GTLibrary import app, db, user_datastore

def _make_context():
    return dict(app=app, db=db, user_datastore=user_datastore, Model=Model)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("runserver", Server(port=app.config['PORT']))
manager.add_command('db', MigrateCommand)

@manager.option('-e', '--email', help='email address')
@manager.option('-p', '--password', help='password')
def create_user(email, password):
    "add a user to the database"
    Model.User.create(email=email, password=password)

@manager.command
def init_db():
    "drop all databases, instantiate schemas"
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def populate_db():
    "insert a default set of objects"
    import GTLibrary.importing as importing
    importing.basic_users()
    #importing.typical_workflow()

if __name__ == "__main__":
    manager.run()
