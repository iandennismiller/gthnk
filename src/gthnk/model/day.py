from __future__ import annotations
from typing import TYPE_CHECKING
import os
from .entry import Entry

if TYPE_CHECKING:
    from .journal import Journal


class Day:
    """
    Represents a single day in a journal.
    """

    def __init__(self, journal:Journal, datestamp:str):
        self.journal = journal
        self.datestamp = datestamp
        self.entries:dict[str, Entry] = {}

    def create_entry(self, timestamp:str, content:str):
        "Create a new entry in the day."
        new_entry = Entry(day=self, timestamp=timestamp, content=content)
        self.entries[timestamp] = new_entry
        return new_entry

    def get_entry(self, timestamp:str):
        "Return an entry by timestamp."
        if timestamp in self.entries:
            return self.entries[timestamp]
        return None

    @property
    def uri(self):
        "Return the URI of the day."
        return os.path.join(self.journal.uri, "day", f"{self.datestamp}.txt")

    @property
    def yesterday(self):
        "Return the previous day."
        return self.journal.get_previous_day(self)

    @property
    def tomorrow(self):
        "Return the next day."
        return self.journal.get_next_day(self)

    def __repr__(self):
        "Return a string representation of the day."
        buf = f"{self.datestamp}\n\n"
        for timestamp in sorted(self.entries.keys()):
            buf += str(self.entries[timestamp])
        return buf
