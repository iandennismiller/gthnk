import os
import logging

from ..filebuffer import FileBuffer


class FileTreeDays(object):
    """
    Represents a full journal as a filesystem tree.
    Works by mapping a journal URI to a filesystem path.
    """

    def __init__(self, filetree):
        self.filetree = filetree
        self.scan_day_ids()

    def get_path_for_day(self, day):
        "Return the filesystem path for a day."
        return os.path.join(self.filetree.path, "day", f".{day.get_uri()}")

    def get_path_for_day_id(self, day_id):
        "Return the filesystem path for a day."
        return os.path.join(self.filetree.path, "day", f"{day_id}.txt")

    def write_day(self, day):
        "Write a day to the filesystem."
        path = self.get_path_for_day(day)
        with open(path, "w") as f:
            f.write(day.__repr__())
        
        for entry in day.entries.values():
            self.filetree.entries.write_entry(entry)

    def read_day_id(self, day_id):
        "Read a day from the filesystem."
        filename = self.get_path_for_day_id(day_id)
        fb = FileBuffer(filename=filename, journal=self.filetree.journal)
        return self.filetree.journal.get_day(day_id)

    def scan_day_ids(self):
        "Scan the filesystem for day ids and create days for them."
        day_ids = []
        logging.getLogger("gthnk").info(f"Scanning {self.filetree.path}/day for days.")
        for filename in os.listdir(os.path.join(self.filetree.path, "day")):
            if filename.endswith(".txt"):
                day_id = filename.replace(".txt", "")
                day_ids.append(day_id)
        for day_id in day_ids:
            if day_id not in self.filetree.journal.days:
                self.filetree.journal.get_day(day_id)
        logging.getLogger("gthnk").info(f"Scanned {len(day_ids)} days from filesystem.")

    def load_all_days(self):
        "Load all days from the filesystem."
        for day_id in self.filetree.journal.days.keys():
            self.read_day_id(day_id)
            logging.getLogger("gthnk").debug(f"Loaded day {day_id} from filesystem.")
