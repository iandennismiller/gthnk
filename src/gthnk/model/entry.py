from __future__ import annotations

import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .day import Day


class Entry:
    """
    Represents a single entry in a journal.
    """

    def __init__(self, day:Day, timestamp:str, content:str=""):
        self.day = day
        self.timestamp = timestamp
        self.content = content

    @property
    def uri(self):
        "Return the URI of the entry."
        return os.path.join(
            self.day.journal.uri,
            "entry",
            self.day.datestamp,
            f"{self.timestamp}.txt"
        )

    def __repr__(self):
        "Return a string representation of the entry."
        return f"{self.timestamp}\n\n{self.content}\n\n"
