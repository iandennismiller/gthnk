# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

# from nose.plugins.attrib import attr
from datetime import datetime
from .mixins import DiamondTestCase
from ..models import Entry, Day


class ModelEntryTestCase(DiamondTestCase):

    def test_create_read(self):
        a_day = Day.create(date=datetime.now())
        obj = Entry.create(day=a_day, content="empty", timestamp=datetime.now())
        print(obj)
        self.assertIsNotNone(obj, "object is created")

        # test retrieval
        entry = Entry.find(content="empty")

        self.assertIsNotNone(entry, "object can be retrieved")
        self.assertEqual(entry.content, "empty", "contains correct value")

    def test_page(self):
        pass
