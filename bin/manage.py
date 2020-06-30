#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import sys
import os
import glob

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
import alembic
import alembic.config

from sqlalchemy.exc import OperationalError

sys.path.insert(0, './src')
from gthnk import db, create_app
from gthnk.models.user import User
from gthnk.adaptors.journal_buffer import JournalBuffer
from gthnk.adaptors.librarian import Librarian


app = create_app()
migrate = Migrate(app, db, directory="gthnk/migrations")


def _make_context():
    return {
        "app": app,
        "db": db,
    }

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("runserver", Server(port=app.config['PORT']))
manager.add_command("publicserver", Server(port=app.config['PORT'], host="0.0.0.0"))
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', help='username', required=True)
@manager.option('-p', '--password', help='password', required=True)
def user_add(username, password):
    "add a user to the database"
    User.create(
        username=username,
        password=password
    )


@manager.option('-u', '--username', help='username', required=True)
def user_del(username):
    "delete a user from the database"
    obj = User.find(username=username)
    if obj:
        obj.delete()
        print("Deleted")
    else:
        print("User not found")


@manager.command
def drop_db():
    "drop all databases, instantiate schemas"
    db.reflect()
    db.drop_all()


@manager.command
def init_db():
    "drop all databases, instantiate schemas"
    db.drop_all()

    # create database from model schema directly
    db.create_all()
    db.session.commit()

    # "stamp" database with version for alembic
    cfg = alembic.config.Config("src/gthnk/migrations/alembic.ini")
    alembic.command.stamp(cfg, "head")


@manager.command
def import_archive(directory):
    with app.app_context():
        journal_buffer = JournalBuffer.TextFileJournalBuffer()
        match_str = os.path.join(directory, "*.txt")
        journal_buffer.process_list(glob.glob(match_str))
        journal_buffer.save_entries()


@manager.command
def journal_export():
    with app.app_context():
        librarian = Librarian(app)
        librarian.export_journal()

if __name__ == "__main__":
    manager.run()
