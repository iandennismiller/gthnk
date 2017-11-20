# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import shutil
import glob
import flask
from nose.plugins.attrib import attr
from .mixins import DiamondTestCase
from ..models import Day, Entry
from ..adaptors.journal_buffer import JournalBuffer, TextFileJournalBuffer


class TestParsing(DiamondTestCase):
    def setUp(self):
        # put an example journal in place
        shutil.copy(
            "gthnk/tests/data/tmp_journal.txt",
            flask.current_app.config["INPUT_FILES"]
        )

        # load some known-correct files
        with open('gthnk/tests/data/correct_output.txt', 'r') as f:
            self.correct_output = ''.join(f.readlines())
        with open('gthnk/tests/data/correct_merge.txt', 'r') as f:
            self.correct_merge = ''.join(f.readlines())
        with open('gthnk/tests/data/two_days_correct.txt', 'r') as f:
            self.correct_twodays = ''.join(f.readlines())
        with open('gthnk/tests/data/2012-10-04.txt', 'r') as f:
            self.correct_04 = ''.join(f.readlines())
        with open('gthnk/tests/data/2012-10-05.txt', 'r') as f:
            self.correct_05 = ''.join(f.readlines())

        super(TestParsing, self).setUp()

    def test_journal_parser(self):
        "Process string parsing."
        journal_buffer = JournalBuffer()
        with open("gthnk/tests/data/source_a.txt", "r") as f:
            journal_buffer.parse(f.read())
        self.assertIsNotNone(journal_buffer.get_entries())

    def test_textfile_parser(self):
        "Process a single file."
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_one("gthnk/tests/data/source_a.txt")
        self.assertIsNotNone(journal_buffer.get_entries(), "process file")

    def test_textfile_batch_parser(self):
        "Process several files."
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list(["gthnk/tests/data/source_a.txt",
            "gthnk/tests/data/source_b.txt"])

        self.assertIsNotNone(journal_buffer.get_entries(), "contents parsed in a small batch")

        comparison = TextFileJournalBuffer()
        comparison.process_one("gthnk/tests/data/source_a.txt")
        comparison.process_one("gthnk/tests/data/source_b.txt")

        self.assertIsNotNone(journal_buffer.dump())

        self.assertEqual(
            journal_buffer.dump(),
            comparison.dump(),
            "contents parsed individually"
        )

    def test_textfile_batch_create(self):
        "Create objects in the database."
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list([
            "gthnk/tests/data/source_a.txt",
            "gthnk/tests/data/source_b.txt"
        ])

        # create objects
        journal_buffer.save_entries()
        self.assertEqual(8, Entry.query.count(), "expected number of objects in DB")

        # use Journal Model to verify that objects were created
        a_day = Day.find(date="2012-10-04")
        self.assertEqual(8, a_day.entries.count(), "expected number of entries returned")

        # and this should not exist
        a_day = Day.find(date="2012-10-05")
        self.assertIsNone(a_day, "there are no entries for the 5th")

    def test_timestamp_ordering(self):
        "timestamps are not in the correct order; should warn about this"
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_one("gthnk/tests/data/out_of_order_times.txt")
        journal_buffer.save_entries()
        self.assertEqual(4, Entry.query.count(), "expected number of objects in DB")

    def test_merge(self):
        "combine two files with interwoven timestamps"
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list(["gthnk/tests/data/source_a.txt",
            "gthnk/tests/data/source_b.txt"])
        journal_buffer.save_entries()
        a_day = Day.find(date="2012-10-04")
        self.assertEqual(a_day.render(), self.correct_merge)

    def test_newlines(self):
        "see if a whole horde of weird newlines screws anything up"
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list(["gthnk/tests/data/excessive_newlines.txt"])
        journal_buffer.save_entries()
        a_day = Day.find(date="2012-10-04")
        self.assertEqual(a_day.render(), self.correct_output)

    def test_twodays(self):
        "ensure journals with several days in them continue to work"
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list(["gthnk/tests/data/two_days.txt"])
        journal_buffer.save_entries()
        self.assertEqual(8, Entry.query.count(), "expected number of objects in DB")

        # now concatenate some days and verify that it matches
        buf = Day.find(date="2012-10-04").render() + \
            Day.find(date="2012-10-05").render() + \
            Day.find(date="2012-10-06").render() + \
            Day.find(date="2012-10-07").render()

        self.assertEqual(buf, self.correct_twodays, "multiple days are output correctly")

    def test_load_smaller_batch(self):
        "load a smaller batch from the archive"
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list(glob.glob("gthnk/tests/data/*.txt"))
        journal_buffer.save_entries()
        self.assertEqual(18, Entry.query.count(), "expected number of entries in DB")
        self.assertEqual(5, Day.query.count(), "expected number of days in DB")

    @attr("skip")
    def test_load_entire_personal_archive(self):
        "load the entire archive"
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list(glob.glob("/Users/idm/Library/Journal/auto/*.txt"))
        journal_buffer.save_entries()
        # self.assertEqual(8, Entry.query.count(), "expected number of objects in DB")

    @attr("skip")
    def test_personal(self):
        "load a smaller batch from the archive"
        journal_buffer = TextFileJournalBuffer()
        journal_buffer.process_list(glob.glob("/Users/idm/Library/Journal/auto/2007-02-0*.txt"))
        journal_buffer.save_entries()
        self.assertEqual(86, Entry.query.count(), "expected number of entries in DB")
        self.assertEqual(7, Day.query.count(), "expected number of days in DB")

    @attr('skip')
    def test_no_date(self):
        "try a file that has no datestamp whatsoever"
        "skipped because I don't know what the correct behaviour is"
        assert False
        # j = Journal("/tmp", self.app)
        # j.parse("gthnk/tests/data/no_date.txt")
        # exported = j.export_week_old()
        # assert exported

    @attr('skip')
    def test_almost_nothing(self):
        "test a file with almost nothing in it"
        "skipped because I don't know what the correct behaviour is"
        assert False
        # j = Journal("/tmp")
        # j.parse("gthnk/tests/data/almost_nothing.txt")
        # exported = j.export_week_old("/tmp")
        # assert exported
