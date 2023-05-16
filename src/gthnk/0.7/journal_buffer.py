# -*- coding: utf-8 -*-
# gthnk (c) 2014-2017 Ian Dennis Miller

import re
import io
import os
import datetime
import sys
import json
from collections import defaultdict
from ..models.entry import Entry


re_day = re.compile(r'^(\d\d\d\d-\d\d-\d\d)\s*$')
re_time = re.compile(r'^(\d\d\d\d)\s*$')
re_time_tag = re.compile(r'^(\d\d\d\d)\s(\w+)\s*$')
re_newlines = re.compile(r'\n\n\n', re.MULTILINE)

def merge_two_dicts(x, y):
    # go through both loops and make a smart merge
    z = y.copy()
    for day in x:
        for timestamp in x[day]:
            z[day][timestamp] += x[day][timestamp]
    return z


def split_filename_list(filename_str):
    """
    """
    return([x.strip() for x in filename_str.split(',')])


def _parse(raw_text):
    """
    parse a Journal-encoded text string; add content to an Entries dictionary, with timestamp.
    """
    entries = defaultdict(lambda: defaultdict(str))

    current_day = None
    current_time = None

    for line in raw_text.splitlines():
        line = line.rstrip()

        match_day = re_day.match(line)
        match_time = re_time.match(line)
        match_time_tag = re_time_tag.match(line)
        tag = ""

        if match_day:
            current_day = match_day.group(1)
            current_time = None
        elif not current_day and line == '':
            # skip blank lines before the first date stamp
            continue
        elif not current_time and line == '':
            continue
        elif current_time and line == '' and current_time not in entries[current_day]:
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
            entries[current_day][current_time] += "{0}\n".format(line)

    for day in entries:
        for timestamp in entries[day]:
            entries[day][timestamp] = entries[day][timestamp].rstrip()
    
    return entries


class JournalBuffer(object):
    """
    A Journal Buffer is an in-memory representation of Journal entries.
    """

    def __init__(self):
        """
        """
        self.entries = defaultdict(lambda: defaultdict(str))

    def parse(self, raw_text):
        if self.entries:
            self.entries = merge_two_dicts(self.entries, _parse(raw_text))
        else:
            self.entries = _parse(raw_text)

    def get_entries(self):
        """
        """
        return(self.entries)

    def render_entries(self):
        buf = ""

        for day in sorted(self.entries.keys()):
            buf += "{}\n\n".format(day)
            for timestamp in sorted(self.entries[day].keys()):
                buf += "{}\n\n".format(timestamp)
                buf += self.entries[day][timestamp]
                buf += "\n\n"
        
        return buf

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
                    flask.current_app.logger.warning("Cannot determine day for '{}' '{}'".format(day, timestamp))
                    continue

                Entry.create(
                    timestamp=time_obj,
                    content=self.entries[day][timestamp]
                )

    def dump(self):
        """
        """
        return(json.dumps(self.get_entries()))

class TextFileJournalBuffer(JournalBuffer):
    """
    provide functions for loading content from a text file
    """
    def process_one(self, filename):
        if os.path.isfile(filename):
            with io.open(filename, "r", encoding="utf-8") as f:
                contents = f.read()
            self.parse(contents)

    def process_list(self, filename_list):
        for filename in filename_list:
            self.process_one(filename)
