# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import shutil
import flask
import warnings
from ..models import User
from flask_testing import TestCase
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)


def setup_journal():
    shutil.copy(
        "gthnk/tests/data/tmp_journal.txt",
        flask.current_app.config["INPUT_FILES"]
    )


def create_user():
    User.register(
        email="guest@example.com",
        password="guest",
        confirmed=True,
        roles=["User"]
    )


class DiamondTestCase(TestCase):
    def create_app(self):
        """
        Create a Flask-Diamond app for testing.

        .
        """
        from .. import create_app
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        """
        Prepare for a test case.

        .
        """
        from .. import db
        from flask import current_app

        db.create_all()
        current_app.logger.debug("setup complete")

    def tearDown(self):
        """
        Clean up after a test case.

        .
        """
        from .. import db
        db.session.remove()
        db.drop_all()
