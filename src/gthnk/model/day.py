from __future__ import annotations

import os

from .entry import Entry

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .journal import Journal
    from .entry import Entry


class Day(object):
    def __init__(self, journal:Journal, datestamp:str):
        self.journal = journal
        self.datestamp = datestamp
        self.entries:dict[str, Entry] = {}

    def create_entry(self, timestamp:str, content:str):
        new_entry = Entry(day=self, timestamp=timestamp, content=content)
        self.entries[timestamp] = new_entry
        return new_entry

    def get_entry(self, timestamp:str):
        if timestamp in self.entries:
            return self.entries[timestamp]

    @property
    def uri(self):
        return os.path.join(self.journal.uri, "day", f"{self.datestamp}.txt")

    @property
    def yesterday(self):
        return self.journal.get_previous_day(self)

    @property
    def tomorrow(self):
        return self.journal.get_next_day(self)

    def __repr__(self):
        buf = f"{self.datestamp}\n\n"
        for timestamp in sorted(self.entries.keys()):
            buf += str(self.entries[timestamp])
        return buf
