# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

# import shutil
# import glob
# import flask
# from nose.plugins.attrib import attr
from .mixins import DiamondTestCase
# from ..models import Day, Entry
# from ..adaptors.journal_buffer import JournalBuffer, TextFileJournalBuffer


class TestLibrarian(DiamondTestCase):
    def setUp(self):
        pass
        # # put an example journal in place
        # shutil.copy(
        #     "gthnk/tests/data/tmp_journal.txt",
        #     flask.current_app.config["INPUT_FILES"]
        # )

        # # load some known-correct files
        # with open('gthnk/tests/data/correct_output.txt', 'r') as f:
        #     self.correct_output = ''.join(f.readlines())
        # with open('gthnk/tests/data/correct_merge.txt', 'r') as f:
        #     self.correct_merge = ''.join(f.readlines())
        # with open('gthnk/tests/data/two_days_correct.txt', 'r') as f:
        #     self.correct_twodays = ''.join(f.readlines())
        # with open('gthnk/tests/data/2012-10-04.txt', 'r') as f:
        #     self.correct_04 = ''.join(f.readlines())
        # with open('gthnk/tests/data/2012-10-05.txt', 'r') as f:
        #     self.correct_05 = ''.join(f.readlines())

        # super(TestParsing, self).setUp()

    def test_librarian(self):
        "Process string parsing."
        pass
        # journal_buffer = JournalBuffer()
        # with open("gthnk/tests/data/source_a.txt", "r") as f:
        #     journal_buffer.parse(f.read())
        # self.assertIsNotNone(journal_buffer.get_entries())
