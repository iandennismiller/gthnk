# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import warnings
from flask_testing import TestCase
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)


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
