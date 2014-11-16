# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import json, os, re
from collections import defaultdict

def split_filename_list(filename_str):
    [x.strip() for x in filename_str.split(',')]

class JournalBuffer(object):
    """
    A Journal Buffer is an in-memory representation of Journal entries.
    """

    def __init__(self):
        self.entries = defaultdict(lambda : defaultdict(str))
        self.re_day = re.compile(r'^(\d\d\d\d-\d\d-\d\d)$')
        self.re_time = re.compile(r'^(\d\d\d\d)$')
        self.re_time_tag = re.compile(r'^(\d\d\d\d)\s(\w+)$')
        self.re_newlines = re.compile(r'\n\n\n', re.MULTILINE)

    def parse(self, raw_text):
        "parse a Journal-encoded text string; add content to an Entries dictionary, with timestamp."
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

    def dump(self):
        buf = ""
        for day in sorted(self.entries.keys()):
            buf += self.dump_day(day)
        return buf

    def dump_day(self, day):
        buf = "%s" % day
        for timestamp in sorted(self.entries[day].keys()):
            buf += "\n\n%s\n\n" % timestamp
            buf += self.entries[day][timestamp]
        buf += "\n"
        return buf

    def list_recent_days(self, num_days):
        """
        get a list of timestamps pertaining to [num_days] recent days
        """
        included = []
        week_ago = datetime.date.today() - datetime.timedelta(days=num_days)
        for day in sorted(self.entries.keys()):
            date = datetime.datetime.strptime(day, '%Y-%m-%d').date()
            if week_ago <= date:
                included.append(day)
        return included

    def get_recent_days(self, num_days):
        """
        retrieve the text from [num_days] recent days
        """
        buf = ""
        week_ago = datetime.date.today() - datetime.timedelta(days=num_days)
        for day in sorted(self.entries.keys()):
            date = datetime.datetime.strptime(day, '%Y-%m-%d').date()
            if week_ago <= date:
                if buf == "":
                    buf += self.dump_day(day)
                else:
                    buf += "\n" + self.dump_day(day)
        return buf

    def get_tag(self, tagname):
        results = []
        for day in self.entries:
            for timestamp in self.entries[day]:
                match_time_tag = re_time_tag.match(timestamp)
                if match_time_tag and match_time_tag.group(2) == tagname:
                    results.append(self.entries[day][timestamp])
        return results

class TextFileJournalBuffer(JournalBuffer):
    """
    provide functions for loading content from a text file
    """
    def process_one(self, filename):
        with open(filename, "r") as f:
            contents = f.read()
        self.parse(contents)

    def process_list(self, filename_list):
        for filename in filename_list:
            self.process_one(filename)
