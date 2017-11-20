# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import shutil
import flask
# from nose.plugins.attrib import attr
from .mixins import DiamondTestCase
from ..models import User


def create_user():
    User.register(
        email="guest@example.com",
        password="guest",
        confirmed=True,
        roles=["User"]
    )


class ViewTestCase(DiamondTestCase):

    def test_login_redirect(self):
        with self.app.test_client() as c:
            rv = c.get('/', follow_redirects=True)
            self.assertIsNotNone(rv.data, "object can be retrieved")
            self.assertRegexpMatches(rv.data, r'Login', "response contains text 'Login'")

    # @attr('single')
    def test_login(self):
        create_user()
        with self.app.test_client() as c:
            rv = c.post('/user/login', data=dict(
                email="guest@example.com",
                password="guest"
            ), follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'logout', "response contains text 'logout'")

    def test_bypass_login(self):
        create_user()
        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True
            rv = c.get('/', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'logout', "response contains text 'logout'")

    def test_refresh(self):
        create_user()
        shutil.copy(
            "gthnk/tests/data/tmp_journal.txt",
            flask.current_app.config["INPUT_FILES"]
        )

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True
            rv = c.get('/', follow_redirects=True)
            rv = c.get('/admin/journal/refresh', follow_redirects=True)
            rv = c.get('/admin/journal/day/2012-10-03.html', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'graduate management consulting association',
                "journal was loaded")

# navigation
#     @expose("/nearest/<date>")
#     @expose("/latest.html")
#     @expose("/search")

# representations
#     @expose("/day/<date>.html")
#     @expose("/text/<date>.txt")
#     @expose("/markdown/<date>.md")
#     @expose("/download/<date>.pdf")

# attachments
#     @expose("/inbox/<date>", methods=['POST'])
#     @expose("/thumbnail/<date>-<sequence>.jpg")
#     @expose("/preview/<date>-<sequence>.jpg")
#     @expose("/attachment/<date>-<sequence>.<extension>")

# attachment management
#     @expose("/day/<date>/attachment/<sequence>/move_up")
#     @expose("/day/<date>/attachment/<sequence>/move_down")
#     @expose("/day/<date>/attachment/<sequence>/delete")
