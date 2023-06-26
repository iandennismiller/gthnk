import re

from .day import Day


class Journal(object):
    def __init__(self, gthnk=None):
        self.days = {}
        self.gthnk = gthnk

    def get_day(self, datestamp:str):
        if datestamp not in self.days:
            new_day = Day(journal=self, datestamp=datestamp)
            self.days[datestamp] = new_day

        return self.days[datestamp]

    def get_entry(self, datestamp:str, timestamp:str):
        day = self.get_day(datestamp)
        return day.get_entry(timestamp)

    @property
    def uri(self):
        return "/"

    def get_latest_datestamp(self):
        "obtain the datestamp (a string) for the latest day in the journal"
        return max(self.days.keys())
    
    def get_latest_day(self):
        "obtain the latest day in the journal"
        return self.get_day(self.get_latest_datestamp())

    def get_previous_day(self, day:Day):
        # first find the index of the day in the sorted list
        sorted_days = sorted([key for key, value in self.days.items() if len(value.entries) > 0])
        index = sorted_days.index(day.datestamp)

        # if the day is already the first day
        if index == 0:
            return None
        else:
            # return the day before that
            return self.days[sorted_days[index - 1]]

    def get_next_day(self, day:Day):
        # first find the index of the day in the sorted list
        sorted_days = sorted([key for key, value in self.days.items() if len(value.entries) > 0])
        index = sorted_days.index(day.datestamp)

        # if the day is already the last day
        if index == len(sorted_days) - 1:
            return None
        else:
            # return the day after that
            return self.days[sorted_days[index + 1]]

    def search(self, query:str, chronological:bool=False):
        query = query.lower()
        self.gthnk.logger.info(f"Searching for {query}")

        # by default we want to search more recent first (i.e. not chronological; reversed)
        for day in sorted(self.days.values(), key=lambda x: x.datestamp, reverse=not chronological):
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
    
    def __getitem__(self, key:str):
        return self.days[key]
    
    def __setitem__(self, key:str, value:str):
        self.days[key] = value
    
    def __delitem__(self, key:str):
        del self.days[key]
    
    def __copy__(self):
        return self.days.copy()
