import os

from .model.journal import Journal
from .filebuffer import FileBuffer


class FileTree(object):
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
        # ensure day path exists as subdirectory of root
        day_path = os.path.join(self.path, "day")
        if not os.path.exists(day_path):
            os.makedirs(day_path)
        # ensure entry path exists as subdirectory of root
        entry_path = os.path.join(self.path, "entry")
        if not os.path.exists(entry_path):
            os.makedirs(entry_path)
        # ensure backup path exists as subdirectory of root
        backup_path = os.path.join(self.path, "backup")
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        self.scan_day_ids()

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

    def get_path_for_day(self, day):
        "Return the filesystem path for a day."
        return os.path.join(self.path, "day", f".{day.get_uri()}")

    def get_path_for_day_id(self, day_id):
        "Return the filesystem path for a day."
        return os.path.join(self.path, "day", f"{day_id}.txt")

    def get_path_for_entry(self, entry):
        "Return the filesystem path for an entry."
        return os.path.join(self.path, "entry", f".{entry.get_uri()}")

    def get_path_for_entry_id(self, day_id, timestamp):
        "Return the filesystem path for an entry."
        return os.path.join(self.path, "entry", f"{day_id}/{timestamp}.txt")

    def ensure_path_for_entry(self, entry):
        "Ensure that a path exists."
        path = self.get_path_for_entry(entry)
        dirname = os.path.dirname(path)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def write_day(self, day):
        "Write a day to the filesystem."
        path = self.get_path_for_day(day)
        with open(path, "w") as f:
            f.write(day.__repr__())
        
        for entry in day.entries.values():
            self.write_entry(entry)

    def write_entry(self, entry):
        "Write an entry to the filesystem."
        self.ensure_path_for_entry(entry)
        path = self.get_path_for_entry(entry)
        with open(path, "w") as f:
            f.write(f"{entry.day.day_id}\n\n{entry.timestamp}\n\n{entry.content}")

    def write_journal(self):
        "Update the filetree with the contents of the journal."
        for day in self.journal:
            self.write_day(day)

    def read_day_id(self, day_id):
        "Read a day from the filesystem."
        filename = self.get_path_for_day_id(day_id)
        fb = FileBuffer(filename=filename, journal=self.journal)
        return self.journal.get_day(day_id)

    def read_entry_id(self, day_id, timestamp):
        "Read an entry from the filesystem."
        # day = self.journal.get_day(day_id)
        filename = self.get_path_for_entry_id(day_id, timestamp)
        fb = FileBuffer(filename=filename, journal=self.journal)
        return self.journal.get_day(day_id, timestamp)

    def scan_day_ids(self):
        "Scan the filesystem for day ids and create days for them."
        day_ids = []
        self.journal.logger.info(f"Scanning {self.path}/day for days.")
        for filename in os.listdir(os.path.join(self.path, "day")):
            if filename.endswith(".txt"):
                day_id = filename.replace(".txt", "")
                day_ids.append(day_id)
        for day_id in day_ids:
            if day_id not in self.journal.days:
                self.journal.get_day(day_id)
        self.journal.logger.info(f"Scanned {len(day_ids)} days from filesystem.")

    def load_all_days(self):
        "Load all days from the filesystem."
        for day_id in self.journal.days.keys():
            self.read_day_id(day_id)
            self.journal.logger.debug(f"Loaded day {day_id} from filesystem.")

    def write_artifact(self, artifact):
        "Write a artifact to the filesystem."
        pass

    def read_artifact(self, artifact_id):
        "Read a artifact from the filesystem."
        pass
