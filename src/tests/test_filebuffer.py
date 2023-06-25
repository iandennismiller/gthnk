import os
import pytest

from gthnk.filebuffer import FileBuffer


def test_filebuffer(cwd, journal):
    fb = FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=journal)
    assert fb

def test_read(cwd, journal):
    
    fb = FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=journal)
    updated_journal = fb.read()
    assert updated_journal
    assert len(updated_journal.days) == 1

def test_backup(cwd, filetree):
    buffer = FileBuffer(f"{cwd}/data/2012-10-04.txt", journal=filetree.journal)
    buffer.read()

    # write the journal to the filesystem
    filetree.write_journal()
    assert os.path.exists("/tmp/gthnk/day/2012-10-04.txt")

    # count number of files in /tmp/gthnk/backup; should be none
    assert len(os.listdir("/tmp/gthnk/backup")) == 0

    # do the backup and ensure one file is created
    buffer.backup()
    assert len(os.listdir("/tmp/gthnk/backup")) == 1

def test_clear(cwd, journal):
    with open("/tmp/gthnk/journal.txt", 'w') as f:
        f.write("1999-12-31\n\n2359\n\nA test entry.\n")
    fb = FileBuffer("/tmp/gthnk/journal.txt", journal=journal)
    fb.clear()
    with open("/tmp/gthnk/journal.txt", 'r') as f:
        assert f.read() == ""
