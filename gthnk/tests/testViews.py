# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from nose.plugins.attrib import attr
from datetime import datetime
import os, shutil, tempfile, sys, unittest, json
from flask.ext.diamond.utils.testhelpers import GeneralTestCase
from Gthnk import Models

class ViewTestCase(GeneralTestCase):
    def setUp(self):
        # fresh testing database
        db.drop_all()
        db.create_all()

        # here, load some data
        with app.app_context():
            user_datastore.create_user(email='admin', password='aaa')
            db.session.commit()

    def tearDown(self):
        db.session.remove()

    @attr('skip')
    def test_index(self):
        with app.test_client() as c:
            rv = c.get('/', follow_redirects=True)
            # assert redirect
            assert 'Login' in rv.data

            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True

            rv = c.get('/')
            assert 'Login' in rv.data

    @attr('online')
    def test_recruit_post(self):
        pass

if __name__ == '__main__':
    unittest.main()