# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import shutil
import flask
import warnings
from flask_testing import TestCase


def setup_journal():
    shutil.copy(
        "tests/data/tmp_journal.txt",
        flask.current_app.config["INPUT_FILES"]
    )


def create_user():
    from gthnk.models.user import User
    User.create(
        username="gthnk",
        password="gthnk"
    )


class CustomTestCase(TestCase):
    def create_app(self):
        """
        Create a Flask-Diamond app for testing.

        .
        """
        from gthnk import create_app
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        """
        Prepare for a test case.

        .
        """
        from gthnk import db
        from flask import current_app

        db.create_all()
        current_app.logger.debug("setup complete")

    def tearDown(self):
        """
        Clean up after a test case.

        .
        """
        from gthnk import db
        db.session.remove()
        db.drop_all()
