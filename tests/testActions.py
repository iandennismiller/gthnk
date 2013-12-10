from nose.tools import assert_equal, assert_not_equal, assert_raises, raises, with_setup
from nose.plugins.attrib import attr

from unittest import TestCase
import os, shutil
from journal.base import Journal
from journal.todo import Todo

class TestActions(TestCase):
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

