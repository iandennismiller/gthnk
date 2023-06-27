import os

from gthnk import Gthnk
from gthnk.model.journal import Journal
from gthnk.filetree.buffer import FileBuffer


def test_journal(gthnk):
    j = Journal()
    assert j is not None

    j = Journal(gthnk=gthnk)
    assert j is not None

def test_gthnk(config_tmp):
    g = Gthnk(config=config_tmp)
    assert g.config["INPUT_FILES"] == "/tmp/gthnk/journal.txt"

def test_rotate(cwd, filetree, gthnk):
    buffer_filename = "/tmp/gthnk/journal.txt"
    with open(buffer_filename, 'w') as f:
        f.write("1999-12-31\n\n2359\n\nA test entry.\n")

    rotate_buffers = gthnk.rotate_buffers()

    assert "1999-12-31" in gthnk.journal.days.keys()
    assert os.path.exists("/tmp/gthnk/day/1999-12-31.txt")
    with open(buffer_filename, 'r') as f:
        assert f.read() == ""

def test_search(cwd, journal):
    FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=journal).read()
    FileBuffer(f"{cwd}/data/2012-10-05.txt", journal=journal).read()
    assert len(list(journal.search("mba"))) > 0

def test_nearest_day(cwd, journal):
    FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=journal).read()
    day = journal.get_nearest_day("2012-10-04")
    assert day.datestamp == "2012-10-04"

    day = journal.get_nearest_day("2012-10-03")
    assert day.datestamp == "2012-10-04"

def test_get_day(cwd, journal):
    FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=journal).read()
    day = journal.get_day("2012-10-04")
    assert day

    day = journal.get_day("2012-10-03")
    assert not day
