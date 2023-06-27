from __future__ import annotations

import os
import logging

from .buffer import FileBuffer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..model.day import Day
    from ..model.journal import Journal


class DaysCollection(object):
    """
    Days: a collection of days in the journal.
    Can be used to read and write days to the filesystem.
    """

    def __init__(self, path:str, journal:Journal):
        self.path = path
        self.journal = journal

    def write(self, day:Day):
        "Write a day to the filetree, along with its entries"
        path = os.path.join(self.path, f".{day.uri}")
        with open(path, "w") as f:
            f.write(day.__repr__())

    def read(self, datestamp:str):
        "Read a day from the filesystem, add to journal."
        filename = os.path.join(self.path, "day", f"{datestamp}.txt")
        FileBuffer(filename=filename, journal=self.journal).read()

    def scan(self):
        "Scan the filesystem for day datestamps."
        datestamps = []
        logging.getLogger("gthnk").debug(f"Scanning {self.path}/day for days.")
        for filename in os.listdir(os.path.join(self.path, "day")):
            if filename.endswith(".txt"):
                datestamp = filename.replace(".txt", "")
                datestamps.append(datestamp)
        logging.getLogger("gthnk").debug(f"Scanned {len(datestamps)} days from filesystem.")
        return datestamps
