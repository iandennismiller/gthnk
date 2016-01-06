#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) 2014-2016 Ian Dennis Miller

import sys
import os
import glob
import traceback
sys.path.insert(0, '.')

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
import alembic
import alembic.config

from gthnk import create_app, db, security
app = create_app()


def _make_context():
    return dict(app=app, db=db, user_datastore=security.datastore)

migrate = Migrate(app, db, directory="gthnk/migrations")

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("runserver", Server(port=app.config['PORT']))
manager.add_command("publicserver", Server(port=app.config['PORT'], host="0.0.0.0"))
manager.add_command('db', MigrateCommand)


@manager.option('-e', '--email', help='email address')
@manager.option('-p', '--password', help='password')
@manager.option('-a', '--admin', help='make user an admin user', action='store_true', default=None)
def useradd(email, password, admin):
    "add a user to the database"
    if admin:
        roles = ["Admin"]
    else:
        roles = ["User"]

    from gthnk import models
    models.User.register(
        email=email,
        password=password,
        confirmed=True,
        roles=roles
    )


@manager.option('-e', '--email', help='email address')
def userdel(email):
    "delete a user from the database"
    from gthnk import models
    obj = models.User.find(email=email)
    obj.delete()


@manager.command
def init_db():
    "drop all databases, instantiate schemas"
    db.drop_all()
    db.create_all()
    db.session.commit()
    cfg = alembic.config.Config("gthnk/migrations/alembic.ini")
    alembic.command.stamp(cfg, "head")


@manager.command
def populate_db():
    "insert a default set of objects"
    from gthnk import models
    models.User.register(
        email='admin',
        password='aaa',
        confirmed=True,
        roles=["User", "Admin"],
    )


@manager.command
def import_archive(directory):
    from gthnk.adaptors.journal_buffer import JournalBuffer
    with app.app_context():
        journal_buffer = JournalBuffer.TextFileJournalBuffer()
        match_str = os.path.join(directory, "*.txt")
        journal_buffer.process_list(glob.glob(match_str))
        journal_buffer.save_entries()


@manager.command
def journal_export():
    from gthnk.librarian import Librarian
    with app.app_context():
        librarian = Librarian(app)
        librarian.export_journal()

if __name__ == "__main__":
    try:
        manager.run()
    except Exception, e:
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
        print "Error: %s" % e
        print "Line: %d" % sys.exc_traceback.tb_lineno
