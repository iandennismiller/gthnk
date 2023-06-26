from __future__ import annotations

import os

from .buffer import FileBuffer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..model.entry import Entry
    from ..model.journal import Journal


class EntriesCollection(object):
    """
    Entries: a collection of entries in the journal.
    Can be used to read and write entries to the filesystem.
    """

    def __init__(self, path:str, journal:Journal):
        self.path = path
        self.journal = journal

    def write(self, entry:Entry):
        "Write an entry to the filesystem."
        path = os.path.join(self.path, f".{entry.uri}")

        # ensure container directory exists
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(path, "w") as f:
            f.write(f"{entry.day.datestamp}\n\n{entry.timestamp}\n\n{entry.content}")

    def read(self, datestamp:str, timestamp:str):
        "Read an entry from the filesystem."
        filename = os.path.join(self.path, "entry", f"{datestamp}/{timestamp}.txt")
        FileBuffer(filename=filename, journal=self.journal).read()
        return self.journal.get_day(datestamp)
