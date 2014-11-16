# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import re, json, datetime, os, shutil
from collections import defaultdict

class JournalParser(object):
    """
    parse a Journal-encoded text string; add content to an Entries dictionary, with timestamp.
    """
    def __init__(self):
        #self.app = app
        self.entries = defaultdict(lambda : defaultdict(str))
        self.re_day = re.compile(r'^(\d\d\d\d-\d\d-\d\d)$')
        self.re_time = re.compile(r'^(\d\d\d\d)$')
        self.re_time_tag = re.compile(r'^(\d\d\d\d)\s(\w+)$')
        self.re_newlines = re.compile(r'\n\n\n', re.MULTILINE)

    def parse(self, raw_text):
        current_day = None
        current_time = None

        for line in raw_text.splitlines():
            line = line.rstrip()

            match_day = self.re_day.match(line)
            match_time = self.re_time.match(line)
            match_time_tag = self.re_time_tag.match(line)
            tag = ""

            if match_day:
                current_day = match_day.group(1)
                current_time = None
            elif not current_day and line == '':
                # skip blank lines before the first date stamp
                continue
            elif not current_time and line == '':
                continue
            elif current_time and line == '' and current_time not in self.entries[current_day]:
                # skip blank lines at the beginning of an entry
                continue
            elif match_time:
                #if current_time and int(current_time[:4]) < int(match_time.group(1)):
                #    self.app.logger.warning("times appear to be out of order")
                current_time = match_time.group(1)
            elif match_time_tag:
                current_time = match_time_tag.group(1)
                tag = match_time_tag.group(2)
                current_time = "%s %s" % (current_time, tag)
            else:
                self.entries[current_day][current_time] += "%s\n" % line

        for day in self.entries:
            for timestamp in self.entries[day]:
                self.entries[day][timestamp] = self.entries[day][timestamp].rstrip()

    def get_entries(self):
        return self.entries

    def save_entries(self):
        """
        add the current entries to the database
        """
        for day in entries.keys():
            for timestamp in entries[day].keys():
                print "{} {}".format(day, timestamp)
                #Models.Entry.create(timestamp=None, content=None)
