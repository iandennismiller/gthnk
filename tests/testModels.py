# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import os, shutil, tempfile, sys
from nose.tools import assert_equal, assert_not_equal, assert_raises, raises, with_setup
from nose.plugins.attrib import attr
from unittest import TestCase

sys.path.insert(0, '.')
os.environ['SETTINGS'] = "../etc/testing.conf"
from GT import app, db, user_datastore, Model

class ModelTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_user(self):
        with app.app_context():
            user_datastore.create_user(email='admin', password='aaa')
            db.session.commit()
        newuser = Model.User.find(email='admin')
        assert newuser
        assert newuser.email == 'admin'

    def test_asset(self):
        with app.app_context():
            user_datastore.create_user(email='admin', password='aaa')
            db.session.commit()
        user = Model.User.query.filter_by(email='admin').first()

        a = Model.Asset(owner=user, name='something')
        db.session.add(a)
        db.session.commit()

        something = Model.Asset.query.filter_by(name="something").first()
        assert something
        assert something.name == "something"

if __name__ == '__main__':
    unittest.main()