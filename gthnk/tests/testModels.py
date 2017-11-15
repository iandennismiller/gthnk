# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from nose.plugins.attrib import attr
from datetime import datetime
import os, shutil, tempfile, sys, unittest, json
from .mixins import DiamondTestCase
from ..models import Entry

class ModelEntryTestCase(DiamondTestCase):
    def test_create(self):
        """Models.Entry: object creation"""
        obj = Entry.create(content="empty", timestamp=datetime.now())
        self.assertIsNotNone(obj, "object is created")

    def test_read(self):
        """Models.Entry: object retrieval"""
        # call test_create to make the object
        self.test_create()

        # test retrieval
        entry = Entry.find(content="empty")
        self.assertIsNotNone(entry, "object can be retrieved")
        self.assertEqual(entry.content, "empty", "contains correct value")
