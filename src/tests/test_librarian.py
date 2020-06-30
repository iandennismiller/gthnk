# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import shutil
import glob
import flask
import os
from distutils.dir_util import remove_tree
# from nose.plugins.attrib import attr
from .mixins import DiamondTestCase
from ..models import Day, Entry
from ..adaptors.librarian import Librarian


def rm(path):
    print(path)
    if os.path.isdir(path):
        print("remove")
        remove_tree(path)


def clean_tmp_export(export_path):
    rm(os.path.join(export_path, "attachment"))
    rm(os.path.join(export_path, "day"))
    rm(os.path.join(export_path, "markdown"))
    rm(os.path.join(export_path, "preview"))
    rm(os.path.join(export_path, "text"))
    rm(os.path.join(export_path, "thumbnail"))
    if len(glob.glob(os.path.join(export_path, "*"))) == 0:
        rm(os.path.join(export_path))


class TestLibrarian(DiamondTestCase):
    def setUp(self):
        # put an example journal in place
        shutil.copy(
            "gthnk/tests/data/tmp_journal.txt",
            flask.current_app.config["INPUT_FILES"]
        )

        super(TestLibrarian, self).setUp()

    def test_rotate(self):
        librarian = Librarian(self.app)
        librarian.rotate_buffers()
        self.assertEqual(Day.query.count(), 1, "1 day has been created")
        self.assertEqual(Entry.query.count(), 4, "4 entries have been created")

    def test_export(self):
        export_path = flask.current_app.config["EXPORT_PATH"]
        clean_tmp_export(export_path)

        librarian = Librarian(self.app)
        librarian.rotate_buffers()
        librarian.export_journal()

        self.assertEqual(len(glob.glob(os.path.join(export_path, "*"))),
            6, "correct number of directories created")
        self.assertEqual(len(glob.glob(os.path.join(export_path, "text", "*"))),
            1, "correct number of text files created")
        self.assertEqual(len(glob.glob(os.path.join(export_path, "markdown", "*"))),
            1, "correct number of markdown files created")

        clean_tmp_export(export_path)
