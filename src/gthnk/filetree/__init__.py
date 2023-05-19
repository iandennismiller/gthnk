import os

from ..model.journal import Journal

from .artifacts import FileTreeArtifacts
from .entries import FileTreeEntries
from .days import FileTreeDays


class FileTreeRoot(object):
    """
    Represents a full journal as a filesystem tree.
    Works by mapping a journal URI to a filesystem path.
    """

    def __init__(self, journal:Journal, path:str=None):
        self.journal = journal

        if path is None:
            self.path = "/tmp/gthnk"
        else:
            self.path = path

        # ensure root path exists
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # ensure artifacts path exists as subdirectory of root
        for subdir in ["day", "entry", "backup", "artifact"]:
            path = os.path.join(self.path, subdir)
            if not os.path.exists(path):
                os.makedirs(path)

        self.days = FileTreeDays(self)
        self.entries = FileTreeEntries(self)
        # self.artifacts = FileTreeArtifacts(self)

    def decode_path(self, path):
        "Return the journal object for a given filesystem path."

        # match day path
        if re.match(r"^.*/\d{4}-\d{2}-\d{2}.txt$", path):
            day_id = re.match(r"^.*/(\d{4}-\d{2}-\d{2}).txt$", path).group(1)
            day = self.journal.get_day(day_id)
            return day
        # match entry path
        elif re.match(r"^.*/\d{4}-\d{2}-\d{2}/\d{4}.txt$", path):
            day_id = re.match(r"^.*/(\d{4}-\d{2}-\d{2})/\d{4}.txt$", path).group(1)
            timestamp = re.match(r"^.*/\d{4}-\d{2}-\d{2}/(\d{4}).txt$", path).group(1)
            day = self.journal.get_day(day_id)
            entry = day.get_entry(timestamp)
            return entry

    def get_path(self):
        "Return the filesystem path of the journal."
        return self.path

    def write_journal(self):
        "Update the filetree with the contents of the journal."
        for day in self.journal:
            self.days.write_day(day)
