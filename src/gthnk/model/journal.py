import re

from .day import Day


class Journal(object):
    def __init__(self, logger=None):
        self.days = {}
        if logger:
            self.logger = logger
        else:
            self.logger = lambda x: None

    def get_day(self, day_id):
        if day_id not in self.days:
            new_day = Day(journal=self, day_id=day_id)
            self.days[day_id] = new_day

        return self.days[day_id]

    def get_entry(self, day_id, timestamp_str):
        day = self.get_day(day_id)
        return day.get_entry(timestamp_str)

    def get_uri(self):
        return "/"

    def search(self, query):
        # search days in chronological order
        for day in sorted(self.days.values(), key=lambda x: x.day_id):
            # search entries in chronological order
            for entry in sorted(day.entries.values(), key=lambda x: x.timestamp):
                if re.search(query, entry.content):
                    yield entry

    def __repr__(self):
        buf = ""
        for day_id in sorted(self.days.keys()):
            buf += f"{self.days[day_id]}\n\n"
        return buf

    def __iter__(self):
        return iter(self.days.values())
    
    def __len__(self):
        return len(self.days)
    
    def __getitem__(self, key):
        return self.days[key]
    
    def __setitem__(self, key, value):
        self.days[key] = value
    
    def __delitem__(self, key):
        del self.days[key]
    
    def __copy__(self):
        return self.days.copy()
