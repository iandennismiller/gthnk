import os
import io
import shutil
import logging
import datetime

from ..model.artifact import Artifact


class FileTreeArtifacts(object):
    """
    Represents a collection of artifacts using a filesystem tree.
    Works by mapping an artifact URI to a filesystem path.
    """

    def __init__(self, filetree):
        self.filetree = filetree

    def scan_day_sequence_ids(self):
        "Scan the filesystem for artifact ids"
        day_ids_sequence_ids = {}
        logging.getLogger("gthnk").debug(f"Scanning {self.filetree.path}/artifact for artifacts.")
        # first scan for day ids
        count = 0
        for day_id in os.listdir(os.path.join(self.filetree.path, "artifact")):
            day_ids_sequence_ids[day_id] = []
            # then scan for sequence ids
            for sequence_id in os.listdir(os.path.join(self.filetree.path, "artifact", day_id)):
                day_ids_sequence_ids[day_id].append(sequence_id)
                count += 1
        logging.getLogger("gthnk").debug(f"Scanned {count} artifacts from filesystem.")
        return day_ids_sequence_ids

    def load_all(self):
        "Lazy-load artifacts for each day id and sequence id"
        day_ids_sequence_ids = self.scan_day_sequence_ids()
        count = 0
        for day_id in day_ids_sequence_ids.keys():
            day = self.filetree.journal.get_day(day_id)
            for sequence_id in day_ids_sequence_ids[day_id]:
                self.read_id(day_id, sequence_id, lazy=True)
                count += 1
        logging.getLogger("gthnk").info(f"Loaded {count} artifacts from filesystem.")

    def get_path(self, artifact):
        "Return the filesystem path containing an artifact."
        return os.path.join(self.path, "artifact", artifact.day.day_id, artifact.sequence)

    def get_path_id(self, day_id, sequence):
        "Return the filesystem path containing an artifact."
        return os.path.join(self.filetree.path, "artifact", day_id, sequence)

    def ensure_path(self, artifact):
        "Ensure that a path exists."
        path = self.get_path(artifact)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def write(self, artifact):
        "Write an artifact to the filesystem."
        self.ensure_path(artifact)
        path = self.get_path(artifact)
        filename = os.path.join(path, artifact.filename)

        # if file path exists, do not overwrite
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(artifact.bytesio.read())

    def read_id(self, day_id, sequence, lazy=True):
        "Read a artifact from the filesystem."
        day = self.filetree.journal.get_day(day_id)

        # look in the artifact directory for the file
        artifact_path = self.get_path_id(day.day_id, sequence)

        # the name of the file in artifact_path
        artifact_path_files = os.listdir(artifact_path)
        if len(artifact_path_files) > 0:
            filename = artifact_path_files[0]
        else:
            raise FileNotFoundError(f"Artifact {day_id}/{sequence} not found.")

        artifact = day.get_artifact(sequence, filename)

        if not lazy:
            artifact_filename = os.path.join(artifact_path, filename)
            with open(artifact_filename, 'rb') as f:
                data = io.BytesIO(f.read())
            artifact.set_data(data)
        else:
            data = None

        logging.getLogger("gthnk").debug(f"Loaded {artifact}")
        return artifact

    def import_file(self, filename):
        "Import an artifact into the filetree, then attach to a day in the journal."
        current_day_id = datetime.datetime.now().strftime("%Y-%m-%d")
        sequence_id = self.get_next_sequence_id(current_day_id)
        # copy the file by filename into the artifact directory
        dst = os.path.join(self.filetree.path, "artifact", current_day_id, str(sequence_id), filename)
        shutil.copy(filename, dst)
        # create a new artifact object
        day = self.filetree.journal.get_day(current_day_id)
        artifact = day.get_artifact(sequence_id, filename)
        logging.getLogger("gthnk").info(f"Import {filename} as artifact {artifact}")

    def get_next_sequence_id(self, day_id=None):
        "Get the next artifact sequence for a day."

        # if day is None, use today
        if day_id is None:
            day_id = datetime.datetime.now().strftime("%Y-%m-%d")

        # Then we count the number of folders in artifact/day_id.
        day_artifacts_path = os.path.join(self.filetree.path, "artifact", day_id)

        # if the path does not exist, create it and set sequence to 0
        if not os.path.exists(day_artifacts_path):
            os.makedirs(day_artifacts_path)
            sequence = 0
            os.makedirs(os.path.join(day_artifacts_path, str(sequence)))
            logging.getLogger("gthnk").info(f"Created artifact directory for {day_id} {sequence}.")
            return sequence

        # the path does exist; analyze the subdirectories in it
        day_artifacts = sorted(os.listdir(day_artifacts_path))
        logging.getLogger("gthnk").info(f"Found {len(day_artifacts)} artifact directories for {day_id}.")

        # the path exists, but there are no subdirectories
        if len(day_artifacts) == 0:
            sequence = 0
            os.makedirs(os.path.join(day_artifacts_path, str(sequence)))
            logging.getLogger("gthnk").info(f"Created artifact directory for {day_id} {sequence}.")
            return sequence

        # the path exists, there are subdirectories; check whether the last one is empty
        last_artifact_path = os.path.join(day_artifacts_path, day_artifacts[-1])
        # If the last one in the list is empty, that's the sequence. 
        if len(os.listdir(last_artifact_path)) == 0:
            sequence = int(day_artifacts[-1])
            logging.getLogger("gthnk").info(f"Found empty artifact directory for {day_id} {sequence}.")
        # If it is not empty, increment sequence and create a directory with the sequence id.
        else:
            sequence = len(day_artifacts) # this effectively increments since we start at 0
            os.makedirs(os.path.join(day_artifacts_path, str(sequence)))
            logging.getLogger("gthnk").info(f"Created artifact directory for {day_id} {sequence}.")

        return sequence
