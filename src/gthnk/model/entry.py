from __future__ import annotations

import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .day import Day


class Entry(object):
    def __init__(self, day:Day, timestamp:str, content:str=""):
        self.day = day
        self.timestamp = timestamp
        self.content = content
    
    @property
    def uri(self):
        return os.path.join(self.day.journal.uri, "entry", self.day.datestamp, f"{self.timestamp}.txt")

    def render_standalone(self):
        return f"{self.day.datestamp}\n\n{self.timestamp}\n\n{self.content}\n"

    def __repr__(self):
        return f"{self.timestamp}\n\n{self.content}\n\n"
