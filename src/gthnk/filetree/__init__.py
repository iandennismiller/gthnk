import os
import re
import logging

from ..model.journal import Journal

from .entries import EntriesCollection
from .days import DaysCollection


class FileTree:
    """
    Represents a full journal as a filesystem tree.
    Works by mapping a journal URI to a filesystem path.
    """

    def __init__(self, journal:Journal, path:str=""):
        self.journal = journal

        if path == "":
            if "FILETREE_ROOT" in self.journal.gthnk.config:
                self.path = self.journal.gthnk.config["FILETREE_ROOT"]
            else:
                raise ValueError("No FILETREE_ROOT in config")
        else:
            self.path = path

        # ensure root path exists
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # ensure paths exist as subdirectory of root
        for subdir in ["day", "entry", "backup"]:
            path = os.path.join(self.path, subdir)
            if not os.path.exists(path):
                os.makedirs(path)

        self.days = DaysCollection(self.path, self.journal)
        self.entries = EntriesCollection(self.path, self.journal)

    def write_journal(self):
        "Update the filetree with the contents of the journal."
        for day in self.journal:
            self.days.write(day)

            for entry in day.entries.values():
                self.entries.write(entry)

    def read_journal(self):
        "Load all days from the filesystem."
        datestamps = self.days.scan()
        if len(datestamps) > 0:
            for datestamp in datestamps:
                self.days.read(datestamp)
                logging.getLogger("gthnk").debug("Loaded day %s from filesystem.", datestamp)

            logging.getLogger("gthnk").info("Loaded %d days from filesystem.", len(self.journal.days))
