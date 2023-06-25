import os
import pytest

from gthnk import Gthnk
from gthnk.model.journal import Journal
from gthnk.filebuffer import FileBuffer


def test_journal_obj(gthnk):
    j = Journal()
    assert j is not None

    j = Journal(gthnk=gthnk)
    assert j is not None

def test_gthnk_obj(gthnk, config_tmp):
    assert gthnk is not None
    assert gthnk.config["INPUT_FILES"] == "/tmp/gthnk/journal.txt"

    g = Gthnk(config=config_tmp)
    assert g.config["INPUT_FILES"] == "/tmp/gthnk/journal.txt"

    assert gthnk.journal is not None

def test_import_buffers(cwd, filetree, gthnk):
    with open("/tmp/gthnk/journal.txt", 'w') as f:
        f.write("1999-12-31\n\n2359\n\nA test entry.\n")

    gthnk.import_buffers()
    assert "1999-12-31" in gthnk.journal.days.keys()

def test_gthnk_rotate(cwd, filetree, gthnk):
    buffer_filename = "/tmp/gthnk/journal.txt"
    with open(buffer_filename, 'w') as f:
        f.write("1999-12-31\n\n2359\n\nA test entry.\n")

    rotate_buffers = gthnk.rotate_buffers()

    assert "1999-12-31" in gthnk.journal.days.keys()
    assert os.path.exists("/tmp/gthnk/day/1999-12-31.txt")
    with open(buffer_filename, 'r') as f:
        assert f.read() == ""
