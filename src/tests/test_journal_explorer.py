# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from tests import env_vscode, CustomTestCase, create_user, setup_journal
env_vscode()

import six


class TestJournalExplorer(CustomTestCase):

    def test_refresh(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = '1'
                sess['_fresh'] = True
            rv = c.get('/', follow_redirects=True)
            rv = c.get('/refresh', follow_redirects=True)
            rv = c.get('/day/2012-10-03.html', follow_redirects=True)
            six.assertRegex(self, str(rv.data),
                r'graduate management consulting association',
                "journal was loaded")

    def test_nearest(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/refresh', follow_redirects=True)

            rv = c.get('/nearest/2012-10-03', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03', "load exact date")

            rv = c.get('/nearest/2012-09-01', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03', "request earlier date")

            rv = c.get('/nearest/2012-10-10', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03', "request later date")

    def test_latest(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/refresh', follow_redirects=True)

            rv = c.get('/latest', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03', "request latest.html")

    def test_search(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/refresh', follow_redirects=True)

            rv = c.get('/search?q={q}'.format(q="graduate"), follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03',
                "search for a findable string finds something")

            rv = c.get('/search?q={q}'.format(q="zorkle"), follow_redirects=True)

            self.assertNotRegex(str(rv.data), r'2012-10-03',
                "search for a unfindable string finds nothing")

    def test_representations(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/refresh', follow_redirects=True)

            rv = c.get('/day/2012-10-03.html', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03', "get day as HTML")
            rv = c.get('/day/2012-10-02.html', follow_redirects=True)

            self.assertNotRegex(str(rv.data), r'2012-10-03',
                "get non-existent day as HTML")

            rv = c.get('/day/2012-10-03.txt', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03', "get day as text")
            rv = c.get('/day/2012-10-02.txt', follow_redirects=True)

            self.assertNotRegex(str(rv.data), r'2012-10-03',
                "get non-existent day as text")

            rv = c.get('/day/2012-10-03.md', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'2012-10-03', "get day as markdown")
            rv = c.get('/day/2012-10-02.md', follow_redirects=True)

            self.assertNotRegex(str(rv.data), r'2012-10-03',
                    "get non-existent day as markdown")

            rv = c.get('/day/2012-10-03.pdf', follow_redirects=True)
            six.assertRegex(self, str(rv.data), r'PDF', "get day as PDF")
            self.assertEqual(len(rv.data), 306, "size match on download")

    # TODO: Skipping attachments for now - but will eventually re-enable
    def unsupported_test_attachments(self):
        create_user()
        setup_journal()

        with self.app.test_client() as c:
            with c.session_transaction() as sess:
                sess['_user_id'] = '1'
                sess['_fresh'] = True

            # trigger refresh of journal
            rv = c.get('/refresh', follow_redirects=True)

            # upload small image
            with open("tests/data/gthnk.png", "rb") as f:
                buf = six.BytesIO(f.read())
            rv = c.post('/inbox/2012-10-03', data=dict(
                file=(buf, 'gthnk.png'),
            ), follow_redirects=True)

            # upload big image
            with open("tests/data/gthnk-big.jpg", "rb") as f:
                buf = six.BytesIO(f.read())
            rv = c.post('/inbox/2012-10-03', data=dict(
                file=(buf, 'gthnk-big.jpg'),
            ), follow_redirects=True)

            # thumbnails
            rv = c.get('/thumbnail/2012-10-03-0.jpg', follow_redirects=True)
            self.assertEqual(len(rv.data), 819, "size match on small thumbnail")
            rv = c.get('/thumbnail/2012-10-03-1.jpg', follow_redirects=True)
            self.assertEqual(len(rv.data), 1640, "size match on big thumbnail")

            # previews
            rv = c.get('/preview/2012-10-03-0.jpg', follow_redirects=True)
            self.assertEqual(len(rv.data), 819, "size match on small preview")
            rv = c.get('/preview/2012-10-03-1.jpg', follow_redirects=True)
            self.assertEqual(len(rv.data), 8611, "size match on big preview")

            # attachments
            rv = c.get('/attachment/2012-10-03-0.jpg', follow_redirects=True)
            self.assertEqual(len(rv.data), 7348, "size match on small attachment")
            rv = c.get('/attachment/2012-10-03-1.jpg', follow_redirects=True)
            self.assertEqual(len(rv.data), 27441, "size match on big attachment")

            # download
            rv = c.get('/download/2012-10-03.pdf', follow_redirects=True)
            self.assertEqual(len(rv.data), 17097, "size match on download")

            # attachment management
            rv = c.get('/day/2012-10-03/1/move_up', follow_redirects=True)
            rv = c.get('/day/2012-10-03/0/move_down', follow_redirects=True)
            rv = c.get('/download/2012-10-03.pdf', follow_redirects=True)
            self.assertEqual(len(rv.data), 17097, "size match on download")
            # TODO: need more robust testing of PDF ordering

            from gthnk import Day

            how_many_1 = len(Day.query.filter_by(date='2012-10-03').first().pages)
            self.assertEqual(how_many_1, 2, "there are 2 attachments")

            rv = c.get('/day/2012-10-03/attachment/1/delete', follow_redirects=True)
            how_many_2 = len(Day.query.filter_by(date='2012-10-03').first().pages)
            self.assertEqual(how_many_2, 1, "there is now 1 attachments")
            rv = c.get('/download/2012-10-03.pdf', follow_redirects=True)
            self.assertEqual(len(rv.data), 1596, "size match on download")

            rv = c.get('/day/2012-10-03/attachment/0/delete', follow_redirects=True)
            how_many_3 = len(Day.query.filter_by(date='2012-10-03').first().pages)
            self.assertEqual(how_many_3, 0, "there are no attachments")
            rv = c.get('/download/2012-10-03.pdf', follow_redirects=True)
            self.assertEqual(len(rv.data), 306, "size match on download")
