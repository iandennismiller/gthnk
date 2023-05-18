import os

from .entry import Entry


class Day(object):
    def __init__(self, journal, day_id):
        self.journal = journal
        self.day_id = day_id
        self.entries = {}
        self.artifacts = {}

    def get_entry(self, timestamp_str):
        if timestamp_str is None:
            timestamp_str = "0000"
        if timestamp_str not in self.entries:
            new_entry = Entry(day=self, timestamp=timestamp_str)
            self.entries[timestamp_str] = new_entry

        return self.entries[timestamp_str]

    def get_artifact(self, sequence=None, filename=None):
        if sequence is None:
            sequence = len(self.artifacts)
        sequence_str = str(sequence)
        if sequence_str not in self.artifacts:
            self.artifacts[sequence_str] = Artifact(day=self, sequence=sequence, filename=filename)
        return self.artifacts[sequence_str]

    def get_uri(self):
        return os.path.join(self.journal.get_uri(), f"{self.day_id}.txt")

    def yesterday(self):
        yd = self.journal.get_previous_day(self)
        return yd

    def tomorrow(self):
        return self.journal.get_next_day(self)

    def __repr__(self):
        buf = f"{self.day_id}\n\n"
        if len(self.entries) > 0:
            try: 
                for timestamp in sorted(self.entries.keys()):
                    buf += self.entries[timestamp].__repr__()
            except TypeError:
                breakpoint()
            return buf
