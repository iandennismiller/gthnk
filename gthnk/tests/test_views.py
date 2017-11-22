# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

# from nose.plugins.attrib import attr
from .mixins import DiamondTestCase, create_user
import six


class ViewTestCase(DiamondTestCase):

    def test_login_redirect(self):
        with self.app.test_client() as c:
            rv = c.get('/', follow_redirects=True)
            self.assertIsNotNone(rv.data, "object can be retrieved")
            six.assertRegex(self, str(rv.data), r'Login', "response contains text 'Login'")

    def test_login(self):
        create_user()
        with self.app.test_client() as c:
            rv = c.post('/user/login', data=dict(
                email="guest@example.com",
                password="guest"
            ), follow_redirects=True)
            six.assertRegex(self, str(rv.data), 'logout', "response contains text 'logout'")

    def test_bypass_login(self):
        create_user()
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True
            rv = c.get('/', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'logout', "response contains text 'logout'")
