# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller

import os, shutil, tempfile, sys, unittest, json, datetime
from nose.plugins.attrib import attr
from flask.ext.diamond.utils.testhelpers import GeneralTestCase
from Gthnk import Models, create_app, db
import Gthnk.JournalBuffer

class TestParsing(GeneralTestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False

        # set up database
        self.db = db
        self.db.drop_all()
        self.db.create_all()

        # set up some text files
        shutil.copy("tests/data/tmp_journal.txt", "/tmp/journal.txt")
        with open('tests/data/correct_output.txt', 'r') as f:
            self.correct_output = ''.join(f.readlines())
        with open('tests/data/correct_merge.txt', 'r') as f:
            self.correct_merge = ''.join(f.readlines())
        with open('tests/data/two_days_correct.txt', 'r') as f:
            self.correct_twodays = ''.join(f.readlines())
        with open('tests/data/2012-10-04.txt', 'r') as f:
            self.correct_04 = ''.join(f.readlines())
        with open('tests/data/2012-10-05.txt', 'r') as f:
            self.correct_05 = ''.join(f.readlines())

    def test_journal_parser(self):
        "process string parsing"
        journal_buffer = Gthnk.JournalBuffer.JournalBuffer()
        with open("tests/data/source_a.txt", "r") as f:
            journal_buffer.parse(f.read())
        self.assertIsNotNone(journal_buffer.get_entries())

    def test_textfile_parser(self):
        "process a single file"
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_one("tests/data/source_a.txt")
        self.assertIsNotNone(journal_buffer.get_entries(), "process file")

    def test_textfile_batch_parser(self):
        "process several files"
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_list(["tests/data/source_a.txt", "tests/data/source_b.txt"])

        self.assertIsNotNone(journal_buffer.get_entries(), "contents parsed in a small batch")

        comparison = Gthnk.JournalBuffer.TextFileJournalBuffer()
        comparison.process_one("tests/data/source_a.txt")
        comparison.process_one("tests/data/source_b.txt")
        self.assertEqual(journal_buffer.dump(), comparison.dump(), "contents parsed individually")

    def test_textfile_batch_create(self):
        "create objects in the database"
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_list(["tests/data/source_a.txt", "tests/data/source_b.txt"])

        # create objects
        journal_buffer.save_entries()
        self.assertEqual(8, Gthnk.Models.Entry.query.count(), "expected number of objects in DB")

        # use Journal Model to verify that objects were created
        a_day = Gthnk.Models.Day(2012, 10, 4)
        self.assertEqual(8, a_day.entries.count(), "expected number of entries returned")

        # and this should not exist
        a_day = Gthnk.Models.Day(2012, 10, 5)
        self.assertEqual(0, a_day.entries.count(), "there are no entries for the 5th")

    def test_timestamp_ordering(self):
        "timestamps are not in the correct order; should warn about this"
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_one("tests/data/out_of_order_times.txt")
        journal_buffer.save_entries()
        self.assertEqual(4, Gthnk.Models.Entry.query.count(), "expected number of objects in DB")

    def test_merge(self):
        "combine two files with interwoven timestamps"
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_list(["tests/data/source_a.txt", "tests/data/source_b.txt"])
        journal_buffer.save_entries()
        a_day = Gthnk.Models.Day(2012, 10, 4)
        self.assertEqual(str(a_day), self.correct_merge)

    def test_newlines(self):
        "see if a whole horde of weird newlines screws anything up"
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_list(["tests/data/excessive_newlines.txt"])
        journal_buffer.save_entries()
        a_day = Gthnk.Models.Day(2012, 10, 4)
        self.assertEqual(str(a_day), self.correct_output)

    @attr("single")
    def test_twodays(self):
        "ensure journals with several days in them continue to work"
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_list(["tests/data/two_days.txt"])
        journal_buffer.save_entries()
        self.assertEqual(8, Gthnk.Models.Entry.query.count(), "expected number of objects in DB")

        # now concatenate some days and verify that it matches
        buf = str(Gthnk.Models.Day(2012, 10, 4)) + "\n" + \
            str(Gthnk.Models.Day(2012, 10, 5)) + "\n" + \
            str(Gthnk.Models.Day(2012, 10, 6)) + "\n" + \
            str(Gthnk.Models.Day(2012, 10, 7))
        self.assertEqual(buf, self.correct_twodays, "multiple days are output correctly")

    @attr('skip')
    def test_no_date(self):
        "try a file that has no datestamp whatsoever"
        "skipped because I don't know what the correct behaviour is"
        j = Journal("/tmp", self.app)
        j.parse("tests/data/no_date.txt")
        exported = j.export_week_old()
        assert exported

    @attr('skip')
    def test_almost_nothing(self):
        "test a file with almost nothing in it"
        "skipped because I don't know what the correct behaviour is"
        j = Journal("/tmp")
        j.parse("tests/data/almost_nothing.txt")
        exported = j.export_week_old("/tmp")
        assert exported

