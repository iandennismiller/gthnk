# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from .mixins import DiamondTestCase


class ViewTestCase(DiamondTestCase):

    def test_redirect_login(self):
        with self.app.test_client() as c:
            rv = c.get('/', follow_redirects=True)
            self.assertIsNotNone(rv.data, "object can be retrieved")
            self.assertRegexpMatches(rv.data, r'Login', "response contains text 'Login'")

    @attr('single')
    def test_bypass_login(self):
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True
            rv = c.get('/', follow_redirects=True)
            print(rv.data)
            assert False
            self.assertRegexpMatches(rv.data, r'Login', "response contains text 'Login'")

    @attr('online')
    def test_recruit_post(self):
        pass
