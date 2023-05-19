import os

from ..filebuffer import FileBuffer


class FileTreeEntries(object):
    """
    Represents a full journal as a filesystem tree.
    Works by mapping a journal URI to a filesystem path.
    """

    def __init__(self, filetree):
        self.filetree = filetree

    def get_path(self, entry):
        "Return the filesystem path for an entry."
        return os.path.join(self.filetree.path, f".{entry.uri}")

    def get_path_id(self, day_id, timestamp):
        "Return the filesystem path for an entry."
        return os.path.join(self.filetree.path, "entry", f"{day_id}/{timestamp}.txt")

    def ensure_path(self, entry):
        "Ensure that a path exists."
        path = self.get_path(entry)
        dirname = os.path.dirname(path)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def write(self, entry):
        "Write an entry to the filesystem."
        self.ensure_path(entry)
        path = self.get_path(entry)
        with open(path, "w") as f:
            f.write(f"{entry.day.day_id}\n\n{entry.timestamp}\n\n{entry.content}")

    def read_id(self, day_id, timestamp):
        "Read an entry from the filesystem."
        # day = self.filetree.journal.get_day(day_id)
        filename = self.get_path_id(day_id, timestamp)
        fb = FileBuffer(filename=filename, journal=self.filetree.journal)
        return self.filetree.journal.get_day(day_id, timestamp)
