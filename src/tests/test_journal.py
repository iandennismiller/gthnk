import pytest

from gthnk import Gthnk
from gthnk.model.journal import Journal
from gthnk.filetree import FileTreeRoot
from gthnk.filebuffer import FileBuffer


def test_journal(journal):
    assert journal is not None

def test_gthnk():
    g = Gthnk(config_filename="/Users/idm/Work/gthnk/.env")
    assert g.journal

def test_load_all_days():
    j = Journal()
    # create a filetree and associate it with this journal
    filetree = FileTreeRoot(journal=j, path="/tmp/gthnk")
    filetree.days.load_all_days()
    assert j

def test_initial_structure():
    j = Journal()
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-04.txt", journal=j)

    # load new file buffer and append to existing journal
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-05.txt", journal=j)

    filetree = FileTreeRoot(journal=j, path="/tmp/gthnk")
    filetree.write_journal()

def test_write_day():
    j = Journal()
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-04.txt", journal=j)
    filetree = FileTreeRoot(journal=j)

    day = j.get_day(day_id="2012-10-04")
    print(day.get_entry("1101").get_uri())
    print(filetree.get_path())
    print(filetree.days.get_path_for_day(day))
    filetree.entries.write_entry(day.get_entry("1101"))
    filetree.days.write_day(day)
