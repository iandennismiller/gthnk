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

    def get_latest_day_id(self):
        return max(self.days.keys())
    
    def get_previous_day(self, day):
        # first find the index of the day in the sorted list
        sorted_days = sorted(self.days.keys())
        index = sorted_days.index(day.day_id)

        # if the day is already the first day, return it
        if index == 0:
            return day
        else:
            # return the day before that
            return self.days[sorted_days[index - 1]]

    def get_next_day(self, day):
        # first find the index of the day in the sorted list
        sorted_days = sorted(self.days.keys())
        index = sorted_days.index(day.day_id)

        # if the day is already the last day, return it
        if index == len(sorted_days) - 1:
            return day
        else:
            # return the day after that
            return self.days[sorted_days[index + 1]]

    def search(self, query, chronological=False):
        query = query.lower()
        self.logger.info(f"Searching for {query}")

        # by default, search entries in reverse chronological order
        # the days start sorted chronologically
        sorted_days = sorted(self.days.values(), key=lambda x: x.day_id)
        # but unless we specify that chronological=True, we want the reverse
        if not chronological:
            sorted_days = reversed(sorted_days)

        for day in sorted_days:
            # search entries in chronological order
            for entry in sorted(day.entries.values(), key=lambda x: x.timestamp):
                if re.search(query, entry.content.lower()):
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
