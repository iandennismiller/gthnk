import os

from .entry import Entry


class Day(object):
    def __init__(self, journal, day_id):
        self.journal = journal
        self.day_id = day_id
        self.entries = {}

    def get_entry(self, timestamp_str):
        if timestamp_str is None:
            timestamp_str = "0000"
        if timestamp_str not in self.entries:
            new_entry = Entry(day=self, timestamp=timestamp_str)
            self.entries[timestamp_str] = new_entry

        return self.entries[timestamp_str]

    @property
    def uri(self):
        return os.path.join(self.journal.uri, "day", f"{self.day_id}.txt")

    @property
    def yesterday(self):
        yd = self.journal.get_previous_day(self)
        return yd

    @property
    def tomorrow(self):
        return self.journal.get_next_day(self)

    def __repr__(self):
        buf = f"{self.day_id}\n\n"
        if len(self.entries) > 0:
            for timestamp in sorted(self.entries.keys()):
                buf += self.entries[timestamp].__repr__()
        return buf
