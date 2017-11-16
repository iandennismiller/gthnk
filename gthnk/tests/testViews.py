# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from datetime import datetime
import os, shutil, tempfile, sys, unittest, json
from .mixins import DiamondTestCase

class ViewTestCase(DiamondTestCase):
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
