# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from nose.plugins.attrib import attr
from datetime import datetime
import os, shutil, tempfile, sys, unittest, json
from flask.ext.diamond.utils.testhelpers import GeneralTestCase
from Gthnk import Models

class ModelEntryTestCase(GeneralTestCase):
    def setUp(self):
        self.db.drop_all()
        self.db.create_all()

    def test_create(self):
        """Models.Entry: object creation"""
        obj = Models.Entry.create(content="empty", timestamp=datetime.now())
        self.assertIsNotNone(obj, "object is created")

    def test_read(self):
        """Models.Entry: object retrieval"""
        # call test_create to make the object
        self.test_create()

        # test retrieval
        entry = Models.Entry.find(content="empty")
        self.assertIsNotNone(entry, "object can be retrieved")
        self.assertEqual(entry.content, "empty", "contains correct value")

if __name__ == '__main__':
    unittest.main()
