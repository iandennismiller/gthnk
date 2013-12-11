# (c) 2013 Ian Dennis Miller
# -*- coding: utf-8 -*-

import os, sys, time, json, re
from GT.dashboard import DashboardWidget
from itertools import islice
import GT.journal

# http://stackoverflow.com/questions/260273/most-efficient-way-to-search-the-last-x-lines-of-a-file-in-python
def reversed_lines(file):
    "Generate the lines of file in reverse order."
    part = ''
    for block in reversed_blocks(file):
        for c in reversed(block):
            if c == '\n' and part:
                yield part[::-1]
                part = ''
            part += c
    if part: yield part[::-1]

def reversed_blocks(file, blocksize=4096):
    "Generate blocks of file's contents in reverse order."
    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(blocksize, here)
        here -= delta
        file.seek(here, os.SEEK_SET)
        yield file.read(delta)

class IdeaListsWidget(DashboardWidget):
    # http://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python

    def render(self):
        lists = {}

        #######
        # ideas
        with open("/Users/idm/Library/Journal/lists/ideas.txt", "r") as i:
            ideas = list(line.strip() for line in i.readlines() if line.strip())
            ideas.reverse()
        lists["ideas"] = ideas

        #######
        # themes
        with open("/Users/idm/Library/Journal/lists/themes.txt", "r") as i:
            themes = list(line.strip() for line in i.readlines() if line.strip())
            themes.reverse()
        lists["themes"] = themes

        #######
        # media
        with open("/Users/idm/Library/Journal/lists/media.txt", "r") as i:
            media = list(line.strip() for line in i.readlines() if line.strip())
            media.reverse()
        lists["media"] = media

        #######
        # radar
        with open("/Users/idm/Library/Journal/lists/radar.txt", "r") as i:
            radar = list(line.strip() for line in i.readlines() if line.strip())
            #radar.reverse()
        lists["radar"] = radar

        #######
        # wanna
        with open("/Users/idm/Library/Journal/lists/wanna.txt", "r") as i:
            wanna = list(line.strip() for line in i.readlines() if line.strip())
            wanna.reverse()
        lists["wanna"] = wanna

        # recent log messages
        with open("/var/lib/greenthink-library/app.log", "r") as f:
            a = [l for l in islice(reversed_lines(f), 40)]
            a.reverse()
            lists["log"] = a

        # yesterday
        journal_path = "/Users/idm/Library/Journal"
        export_path = os.path.join(journal_path, "auto")
        live_file = os.path.join(journal_path, 'journal.txt')
        j = GT.journal.Journal(export_path)
        j.parse(live_file)

        buf = j.get_recent_days(1)
        lists['yesterday'] = buf

        return lists
