import os
import shutil

from gthnk.filetree.buffer import FileBuffer


def test_filetree(filetree):
    assert filetree
    assert filetree.path == "/tmp/gthnk"

def test_write_journal(cwd, filetree):
    FileBuffer(f"{cwd}/data/2012-10-05.txt", journal=filetree.journal).read()
    filetree.write_journal()
    assert os.path.exists("/tmp/gthnk/entry/2012-10-05/1103.txt")
    assert os.path.exists("/tmp/gthnk/day/2012-10-05.txt")

def test_read_journal(cwd, filetree):
    "create a filetree and associate it with this journal"
    shutil.copy(f"{cwd}/data/2012-10-04.txt", "/tmp/gthnk/day")
    shutil.copy(f"{cwd}/data/2012-10-05.txt", "/tmp/gthnk/day")
    filetree.read_journal()
    assert len(filetree.journal.days) == 2

def test_initial_structure(filetree):
    # assert the filetree paths exist
    assert os.path.exists("/tmp/gthnk")
    assert os.path.exists("/tmp/gthnk/entry")
    assert os.path.exists("/tmp/gthnk/day")
    assert os.path.exists("/tmp/gthnk/backup")

def test_write_entry(cwd, filetree):
    FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=filetree.journal).read()
    day = filetree.journal.get_day(datestamp="2012-10-04")
    assert day

    filetree.entries.write(day.get_entry("1101"))
    assert os.path.exists("/tmp/gthnk/entry/2012-10-04/1101.txt")

def test_read_day(cwd, filetree):
    FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=filetree.journal).read()
    day = filetree.journal.get_day(datestamp="2012-10-04")
    assert day.datestamp == "2012-10-04"

def test_write_day(cwd, filetree):
    FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=filetree.journal).read()
    day = filetree.journal.get_day(datestamp="2012-10-04")
    filetree.days.write(day)
    assert os.path.exists("/tmp/gthnk/day/2012-10-04.txt")
