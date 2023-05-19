import os
import io
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

    def scan_ids(self):
        "Scan the filesystem for artifact ids and lazy-create artifacts for them."
        pass

    def get_path(self, artifact):
        "Return the filesystem path containing an artifact."
        return os.path.join(self.path, "artifact", artifact.day.day_id, artifact.sequence)

    def get_path_id(self, day_id, sequence):
        "Return the filesystem path containing an artifact."
        return os.path.join(self.path, "artifact", day_id, sequence)

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

    def load(self, filename):
        "Import an artifact into the filetree, then attach to a day in the journal."
        logging.getLogger("gthnk").info(f"Import artifact: {filename}")
        current_day_id = datetime.datetime.now().strftime("%Y-%m-%d")
        sequence = self.get_next_sequence(current_day_id)
        print(sequence)
        breakpoint()

    def get_next_sequence(self, day=None):
        "Get the next artifact sequence for a day."

        # if day is None, use today
        if day is None:
            day_id = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            day_id = day.day_id

        # Then we count the number of folders in artifact/day_id.
        day_artifacts_path = os.path.join(self.path, "artifact", day_id)

        # if the path does not exist, create it and set sequence to 0
        if not os.path.exists(day_artifacts_path):
            os.makedirs(day_artifacts_path)
            sequence = 0
            logging.getLogger("gthnk").info(f"Created artifact directory for {day_id}.")
        else:
            day_artifacts = sorted(os.listdir(day_artifacts_path))
            logging.getLogger("gthnk").info(f"Found {len(day_artifacts)} artifact directories for {day_id}.")

            # check whether the last one is empty
            last_artifact_path = os.path.join(day_artifacts_path, day_artifacts[-1])
            # If the last one in the list is empty, that's the sequence. 
            if len(os.listdir(last_artifact_path) == 0):
                sequence = int(day_artifacts[-1])
                logging.getLogger("gthnk").info(f"Found empty artifact directory for {day_id} {sequence}.")
            else:
                # If it is not empty, increment sequence and create a directory with the sequence id.
                sequence = len(day_artifacts)
                os.makedirs(os.path.join(day_artifacts_path, str(sequence)))
                logging.getLogger("gthnk").info(f"Created artifact directory for {day_id} {sequence}.")

        return sequence
