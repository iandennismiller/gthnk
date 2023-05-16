#!/usr/bin/env python3

import os
from dotenv import load_dotenv

from gthnk.model.journal import Journal
from gthnk.filebuffer import FileBuffer
from gthnk.filetree import FileTree

from gthnk.gthnk import Gthnk

load_dotenv()


def t0():
    g = Gthnk(config_filename=os.getenv("CONFIG_FILENAME"))
    print(g.journal)

def t1():
    j = Journal()
    # create a filetree and associate it with this journal
    filetree = FileTree(journal=j, path="/Users/idm/Work/gthnk/var/gthnk")
    filetree.load_all_days()
    print(j)

def create_initial_structure():
    j = Journal()
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-04.txt", journal=j)

    # load new file buffer and append to existing journal
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-05.txt", journal=j)

    filetree = FileTree(journal=j, path="/Users/idm/Work/gthnk/var/gthnk")
    filetree.write_journal()

def t2():
    j = Journal()
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-04.txt", journal=j)

    # load new file buffer and append to existing journal
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-05.txt", journal=j)

    filetree = FileTree(journal=j)
    filetree.write_journal()

def t3():
    j = Journal()
    fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-04.txt", journal=j)

    day = j.get_day(day_id="2012-10-04")
    print(day.get_entry("1101").get_uri())
    print(j.filetree.get_path())
    print(j.filetree.get_path_for_day(day))
    j.filetree.write_entry(day.get_entry("1101"))
    j.filetree.write_day(day)

if __name__ == "__main__":
    # create_initial_structure()
    t0()
    # t1()
    # t2()
    # t3()
