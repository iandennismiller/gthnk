# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from .mixins import DiamondTestCase, create_user, setup_journal


class ViewTestCase(DiamondTestCase):

    def test_refresh(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True
            rv = c.get('/', follow_redirects=True)
            rv = c.get('/admin/journal/refresh', follow_redirects=True)
            rv = c.get('/admin/journal/day/2012-10-03.html', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'graduate management consulting association',
                "journal was loaded")

    def test_nearest(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/admin/journal/refresh', follow_redirects=True)

            rv = c.get('/admin/journal/nearest/2012-10-03', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03', "load exact date")

            rv = c.get('/admin/journal/nearest/2012-09-01', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03', "request earlier date")

            rv = c.get('/admin/journal/nearest/2012-10-10', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03', "request later date")

    def test_latest(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/admin/journal/refresh', follow_redirects=True)

            rv = c.get('/admin/journal/latest.html', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03', "request latest.html")

    def test_search(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/admin/journal/refresh', follow_redirects=True)

            rv = c.get('admin/journal/search?q={q}'.format(q="graduate"), follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03',
                "search for a findable string finds something")

            rv = c.get('admin/journal/search?q={q}'.format(q="zorkle"), follow_redirects=True)
            self.assertNotRegexpMatches(rv.data, r'2012-10-03',
                "search for a unfindable string finds nothing")

    def test_representations(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/admin/journal/refresh', follow_redirects=True)

            rv = c.get('/admin/journal/day/2012-10-03.html', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03', "get day as HTML")
            rv = c.get('/admin/journal/day/2012-10-02.html', follow_redirects=True)
            self.assertNotRegexpMatches(rv.data, r'2012-10-03', "get non-existent day as HTML")

            rv = c.get('/admin/journal/text/2012-10-03.txt', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03', "get day as text")
            rv = c.get('/admin/journal/text/2012-10-02.txt', follow_redirects=True)
            self.assertNotRegexpMatches(rv.data, r'2012-10-03', "get non-existent day as text")

            rv = c.get('/admin/journal/markdown/2012-10-03.md', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'2012-10-03', "get day as markdown")
            rv = c.get('/admin/journal/markdown/2012-10-02.md', follow_redirects=True)
            self.assertNotRegexpMatches(rv.data, r'2012-10-03', "get non-existent day as markdown")

            rv = c.get('/admin/journal/download/2012-10-03.pdf', follow_redirects=True)
            self.assertRegexpMatches(rv.data, r'PDF', "get day as PDF")

# attachments
#     @expose("/inbox/<date>", methods=['POST'])
#     @expose("/thumbnail/<date>-<sequence>.jpg")
#     @expose("/preview/<date>-<sequence>.jpg")
#     @expose("/attachment/<date>-<sequence>.<extension>")

# attachment management
#     @expose("/day/<date>/attachment/<sequence>/move_up")
#     @expose("/day/<date>/attachment/<sequence>/move_down")
#     @expose("/day/<date>/attachment/<sequence>/delete")
