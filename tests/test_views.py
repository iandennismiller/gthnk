# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from tests import env_vscode, CustomTestCase, create_user
env_vscode()

import six


class TestViews(CustomTestCase):

    def test_login_redirect(self):
        with self.app.test_client() as c:
            rv = c.get('/', follow_redirects=True)
            self.assertIsNotNone(rv.data, "object can be retrieved")
            six.assertRegex(self, str(rv.data), r'Log in', "response contains text 'Log in'")

    def test_login(self):
        create_user()
        self.app.logger.info("created user")
        with self.app.test_client() as c:
            rv = c.post('/login', data=dict(
                username="gthnk",
                password="gthnk"
            ), follow_redirects=True)

            six.assertRegex(self, str(rv.data), 'Logged in successfully.', "response contains login confirmation")

    def test_bypass_login(self):
        create_user()
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = '1'
                sess['_fresh'] = True

            rv = c.get('/', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'logout', "response contains text 'logout'")
