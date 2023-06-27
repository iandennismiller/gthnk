import re

from .day import Day


class Journal:
    """
    Represents a full journal.
    """

    def __init__(self, gthnk=None):
        self.days = {}
        self.gthnk = gthnk

    def create_day(self, datestamp:str):
        "Create a new day in the journal"
        new_day = Day(journal=self, datestamp=datestamp)
        self.days[datestamp] = new_day
        return new_day

    def get_day(self, datestamp:str):
        "Return a day by datestamp"
        if datestamp in self.days:
            return self.days[datestamp]
        return None

    @property
    def uri(self):
        "Return the URI of the journal"
        return "/"

    def get_latest_datestamp(self):
        "obtain the datestamp (a string) for the latest day in the journal"
        return max(self.days.keys())

    def get_latest_day(self):
        "obtain the latest day in the journal"
        return self.get_day(self.get_latest_datestamp())

    def get_previous_day(self, day:Day):
        "obtain the previous day in the journal"
        # first find the index of the day in the sorted list
        sorted_days = sorted([key for key, value in self.days.items() if len(value.entries) > 0])
        index = sorted_days.index(day.datestamp)

        # if the day is already the first day
        if index == 0:
            return None

        # return the day before that
        return self.days[sorted_days[index - 1]]

    def get_next_day(self, day:Day):
        "obtain the next day in the journal"
        # first find the index of the day in the sorted list
        sorted_days = sorted([key for key, value in self.days.items() if len(value.entries) > 0])
        index = sorted_days.index(day.datestamp)

        # if the day is already the last day
        if index == len(sorted_days) - 1:
            return None

        # return the day after that
        return self.days[sorted_days[index + 1]]

    def get_nearest_day(self, datestamp:str):
        "obtain the nearest day in the journal"

        # if the day exists, return it
        if datestamp in self.days and len(self.days[datestamp].entries) > 0:
            return self.days[datestamp]

        # obtain all datestamps, only including days with entries
        datestamps = sorted([key for key, value in self.days.items() if len(value.entries) > 0])
        # iterate sorted list to find first day that is larger
        larger_datestamps = [x for x in datestamps if x > datestamp]

        if larger_datestamps:
            return self.days[larger_datestamps[0]]
        return None

    def search(self, query:str, chronological:bool=False):
        "search the journal for a query string"
        query = query.lower()
        self.gthnk.logger.info(f"Searching for {query}")

        # by default we want to search more recent first (i.e. not chronological; reversed)
        for day in sorted(self.days.values(), key=lambda x: x.datestamp, reverse=not chronological):
            # search entries in chronological order
            for entry in sorted(day.entries.values(), key=lambda x: x.timestamp):
                if re.search(query, entry.content.lower()):
                    yield entry

    def __repr__(self):
        "Return a string representation of the journal."
        buf = ""
        for day_id in sorted(self.days.keys()):
            buf += f"{self.days[day_id]}\n\n"
        return buf

    def __iter__(self):
        "Return an iterator over the days in the journal."
        return iter(self.days.values())

    def __len__(self):
        "Return the number of days in the journal."
        return len(self.days)

    def __getitem__(self, key:str):
        "Return a day by datestamp."
        return self.days[key]

    def __setitem__(self, key:str, value:str):
        "Set a day by datestamp."
        self.days[key] = value

    def __delitem__(self, key:str):
        "Delete a day by datestamp."
        del self.days[key]

    def __copy__(self):
        "Return a copy of the journal."
        return self.days.copy()
