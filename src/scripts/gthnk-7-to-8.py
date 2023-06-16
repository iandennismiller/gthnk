#!/usr/bin/env python3
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

from gthnk.__meta__ import __version__
from gthnk_server import db
from gthnk_7_to_8.server import create_app
from gthnk_7_to_8.models.user import User
from gthnk_7_to_8.models.day import Day
from gthnk_7_to_8.models.entry import Entry
from gthnk_7_to_8.models.page import Page


app = create_app()
migrate = Migrate(app, db, directory="src/gthnk_7_to_8/migrations")


def _make_context():
    return {
        "app": app,
        "db": db,
        "User": User,
        "Day": Day,
        "Entry": Entry,
        "Page": Page
    }

manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


@manager.command
def drop_db():
    """
    drop all databases
    """
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
    cfg = alembic.config.Config("src/gthnk_7_to_8/migrations/alembic.ini")
    alembic.command.stamp(cfg, "head")

@manager.option('-d', '--directory', help='directory', required=True)
def import_archive(directory):
    """
    Import archive of journal files
    """
    with app.app_context():
        journal_buffer = TextFileJournalBuffer()
        match_str = os.path.join(directory, "*.txt")
        journal_buffer.process_list(glob.glob(match_str))
        journal_buffer.save_entries()

@manager.command
def journal_export():
    """
    Export journal files
    """
    with app.app_context():
        librarian = Librarian(app)
        librarian.export_journal()

if __name__ == "__main__":
    manager.run()
