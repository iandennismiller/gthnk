# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from tests import env_vscode, CustomTestCase
env_vscode()

import six
import datetime
import unittest

from gthnk.models.day import Day
from gthnk.models.entry import Entry
from gthnk.models.page import Page

class TestModels(CustomTestCase):

    def test_crud(self):
        "Go through CRUD operations to exercise the models."
        # test create
        day = Day.create(date=datetime.date.today())
        self.assertIsNotNone(day, "Day is created")

        entry = Entry.create(day=day, content="empty", timestamp=datetime.datetime.now())
        self.assertIsNotNone(entry, "Entry is created")

        # attach an image to a day
        with open("tests/data/gthnk-big.jpg", "rb") as f:
            buf = six.BytesIO(f.read())
            page = day.attach(buf.getvalue())
            self.assertIsNotNone(page, "Page is created")

        # test read
        day_find = Day.find(date=datetime.date.today())
        self.assertIsNotNone(day_find, "Day can be retrieved")
        self.assertEqual(day_find.entries[0].content, "empty", "contains correct value")

        entry_find = Entry.find(content="empty")
        self.assertIsNotNone(entry_find, "Entry can be retrieved")
        self.assertEqual(entry_find.content, "empty", "contains correct value")

    # special testing for Page class
    def test_page(self):
        assert Page

    # special testing for Day class
    def test_day(self):
        assert Day

    # special testing for Entry class
    def test_entry(self):
        assert Entry
