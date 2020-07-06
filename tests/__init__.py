# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import sys
import shutil
import flask
from flask_testing import TestCase


def env_vscode():
    "prepare environment so tests can be detected by vscode"
    cwd = os.getcwd()
    os.environ["SETTINGS"] = os.path.join(cwd, "usr/conf/testing.conf")
    sys.path.insert(0, "src")


def setup_journal():
    shutil.copy(
        "tests/data/tmp_journal.txt",
        flask.current_app.config["INPUT_FILES"]
    )


def create_user():
    from gthnk.models.user import User
    User.create_with_password(
        username="gthnk",
        password="gthnk"
    )


class CustomTestCase(TestCase):
    def create_app(self):
        """
        Create a Flask-Diamond app for testing.

        .
        """
        from gthnk.server import create_app
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.logger.info("finish create_app()")

        return app

    def setUp(self):
        """
        Prepare for a test case.

        .
        """
        from gthnk import db
        from flask import current_app

        db.create_all()
        current_app.logger.info("setup complete")

    def tearDown(self):
        """
        Clean up after a test case.

        .
        """
        from gthnk import db
        db.session.remove()
        db.drop_all()
