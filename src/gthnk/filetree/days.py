from __future__ import annotations
from typing import TYPE_CHECKING
import os
import logging

from .buffer import FileBuffer

if TYPE_CHECKING:
    from ..model.day import Day
    from ..model.journal import Journal


class DaysCollection:
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
        with open(path, "w", encoding="utf-8") as file_handle:
            file_handle.write(str(day))

    def read(self, datestamp:str):
        "Read a day from the filesystem, add to journal."
        filename = os.path.join(self.path, "day", f"{datestamp}.txt")
        FileBuffer(filename=filename, journal=self.journal).read()

    def scan(self):
        "Scan the filesystem for day datestamps."
        datestamps = []
        logging.getLogger("gthnk").debug("Scanning %s/day for days.", self.path)
        for filename in os.listdir(os.path.join(self.path, "day")):
            if filename.endswith(".txt"):
                datestamp = filename.replace(".txt", "")
                datestamps.append(datestamp)
        logging.getLogger("gthnk").debug("Scanned %d days from filesystem.", len(datestamps))
        return datestamps
