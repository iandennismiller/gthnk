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
from .utils import merge_two_dicts, split_filename_list
from .journal_format import _parse


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
