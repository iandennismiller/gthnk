# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

from tests import env_vscode, CustomTestCase
env_vscode()

import os
import glob
import flask
import shutil
from distutils.dir_util import remove_tree

from gthnk.models.day import Day
from gthnk.models.entry import Entry
from gthnk.librarian import Librarian


def rm(path):
    if os.path.isdir(path):
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


class TestLibrarian(CustomTestCase):
    def setUp(self):
        # put an example journal in place
        shutil.copy(
            "tests/data/tmp_journal.txt",
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
