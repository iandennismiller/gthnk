# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import os, shutil, tempfile, sys
from nose.tools import assert_equal, assert_not_equal, assert_raises, raises, with_setup
from nose.plugins.attrib import attr
from unittest import TestCase

sys.path.insert(0, '.')
os.environ['SETTINGS'] = "../etc/testing.conf"
from GT import app, db, user_datastore, Model

class ViewTestCase(TestCase):

    def setUp(self):
        app.config['TESTING'] = True

        # fresh testing database
        db.drop_all()
        db.create_all()
        db.session.commit()

        # here, load some data
        user_datastore.create_user(email='admin', password='aaa')
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_index(self):
        with app.test_client() as c:
            rv = c.get('/', follow_redirects=True)
            # assert redirect
            assert 'Login' in rv.data

            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True

            rv = c.get('/')
            assert 'index' in rv.data

    @attr('online')
    def test_recruit_post(self):
        pass

if __name__ == '__main__':
    unittest.main()