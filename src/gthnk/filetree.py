import os
import io

from .model.journal import Journal
from .model.artifact import Artifact
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

        # ensure artifacts path exists as subdirectory of root
        for subdir in ["day", "entry", "backup", "artifact"]:
            path = os.path.join(self.path, subdir)
            if not os.path.exists(path):
                os.makedirs(path)

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

    ###
    # Artifacts

    def scan_artifact_ids(self):
        "Scan the filesystem for artifact ids and lazy-create artifacts for them."
        pass

    def get_path_for_artifact(self, artifact):
        "Return the filesystem path containing an artifact."
        return os.path.join(self.path, "artifact", artifact.day.day_id, artifact.sequence)

    def get_path_for_artifact_id(self, day_id, sequence):
        "Return the filesystem path containing an artifact."
        return os.path.join(self.path, "artifact", day_id, sequence)

    def ensure_path_for_artifact(self, artifact):
        "Ensure that a path exists."
        path = self.get_path_for_artifact(artifact)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def write_artifact(self, artifact):
        "Write an artifact to the filesystem."
        self.ensure_path_for_artifact(artifact)
        path = self.get_path_for_artifact(artifact)
        filename = os.path.join(path, artifact.filename)

        # if file path exists, do not overwrite
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(artifact.bytesio.read())

    def read_artifact(self, day_id, sequence, lazy=True):
        "Read a artifact from the filesystem."
        day = self.journal.get_day(day_id)

        # look in the artifact directory for the file
        artifact_path = self.get_path_for_artifact_id(day.day_id, sequence)

        # the name of the file in artifact_path
        artifact_path_files = os.listdir(artifact_path)
        if len(artifact_path_files) > 0:
            filename = [0]
        else:
            raise FileNotFoundError(f"Artifact {day_id}/{sequence} not found.")

        if not lazy:
            artifact_filename = os.path.join(artifact_path, filename)
            with open(artifact_filename, 'rb') as f:
                data = io.BytesIO(f.read())
        else:
            data = None

        artifact = Artifact(day=day, sequence=sequence, filename=filename, data=data)
        return artifact

    def import_artifact(self, filename):
        "Import an artifact into the filetree, then attach to a day in the journal."
        self.journal.logger.info(f"Import artifact: {filename}")
        current_day_id = datetime.datetime.now().strftime("%Y-%m-%d")
        sequence = self.journal.get_next_sequence(current_day_id)
