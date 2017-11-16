# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from nose.plugins.attrib import attr
from datetime import datetime
import os, shutil, tempfile, sys, unittest, json
from .mixins import DiamondTestCase
from ..models import Entry, Day

class ModelEntryTestCase(DiamondTestCase):

    def test_createread(self):
        a_day = Day.create(date=datetime.now())
        obj = Entry.create(day=a_day, content=unicode("empty"), timestamp=datetime.now())
        print(obj)
        self.assertIsNotNone(obj, "object is created")

        # test retrieval
        entry = Entry.find(content=unicode("empty"))

        self.assertIsNotNone(entry, "object can be retrieved")
        self.assertEqual(entry.content, unicode("empty"), "contains correct value")
