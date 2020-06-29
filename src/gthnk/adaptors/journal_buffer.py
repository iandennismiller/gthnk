# -*- coding: utf-8 -*-
# gthnk (c) 2014-2017 Ian Dennis Miller

import re
import io
import datetime
import sys
from collections import defaultdict
from gthnk import models


def split_filename_list(filename_str):
    """
    """
    return([x.strip() for x in filename_str.split(',')])


class JournalBuffer(object):
    """
    A Journal Buffer is an in-memory representation of Journal entries.
    """

    def __init__(self):
        """
        """
        PY3 = sys.version_info[0] > 2
        if PY3:
            self.entries = defaultdict(lambda: defaultdict(str))
        else:
            self.entries = defaultdict(lambda: defaultdict(unicode))
        self.re_day = re.compile(r'^(\d\d\d\d-\d\d-\d\d)\s*$')
        self.re_time = re.compile(r'^(\d\d\d\d)\s*$')
        self.re_time_tag = re.compile(r'^(\d\d\d\d)\s(\w+)\s*$')
        self.re_newlines = re.compile(r'\n\n\n', re.MULTILINE)

    def parse(self, raw_text):
        """
        parse a Journal-encoded text string; add content to an Entries dictionary, with timestamp.
        """
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
                #current_time = "%s %s" % (current_time, tag)
            else:
                self.entries[current_day][current_time] += "{0}\n".format(line)

        for day in self.entries:
            for timestamp in self.entries[day]:
                self.entries[day][timestamp] = self.entries[day][timestamp].rstrip()

    def get_entries(self):
        """
        """
        return(self.entries)

    def save_entries(self):
        """
        add the current entries to the database
        """
        for day in self.entries.keys():
            for timestamp in self.entries[day].keys():
                try:
                    time_obj = datetime.datetime.strptime(
                        "{} {}".format(day, timestamp), '%Y-%m-%d %H%M')
                except:
                    import flask
                    flask.current_app.logger.warn("Cannot determine day for '{}' '{}'".format(day, timestamp))
                    continue

                models.Entry.create(
                    timestamp=time_obj,
                    content=self.entries[day][timestamp]
                )

    def dump(self):
        """
        """
        import json
        return(json.dumps(self.get_entries()))

class TextFileJournalBuffer(JournalBuffer):
    """
    provide functions for loading content from a text file
    """
    def process_one(self, filename):
        with io.open(filename, "r", encoding="utf-8") as f:
            contents = f.read()
        self.parse(contents)

    def process_list(self, filename_list):
        for filename in filename_list:
            self.process_one(filename)
