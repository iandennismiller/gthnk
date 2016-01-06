# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

from nose.plugins.attrib import attr
from datetime import datetime
import os, shutil, tempfile, sys, unittest, json
from flask.ext.diamond.utils.testhelpers import GeneralTestCase

#from GT.journal import Journal
#from GT.journal.todo import Todo

class TestActions(GeneralTestCase):
    def setUp(self):
        "set up test fixtures"
        shutil.copy("tests/data/tmp_journal.txt", "/tmp/journal.txt")

    def teardown(self):
        "tear down test fixtures"
        pass

    @attr('online')
    def test_todo_action(self):
        j = Journal("/tmp")
        toodledo = Todo(debug=True)
        j.parse("tests/data/todo.txt")
        todo_items = j.get_tag("todo")
        assert_equal(len(todo_items), 2)

    @attr('online')
    def test_shopping_action(self):
        j = Journal("/tmp")
        toodledo = Shopping(debug=True)
        j.parse("tests/data/todo.txt")
        todo_items = j.get_tag("todo")
        assert_equal(len(todo_items), 2)

