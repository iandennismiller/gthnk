import os
import io


class Artifact(object):
    def __init__(self, day, sequence, filename, data:io.BytesIO=None):
        self.day = day
        self.sequence = sequence
        self.filename = filename
        self._data = data
    
    @property
    def uri(self):
        "return the URI of the artifact"
        return os.path.join(self.day.journal.uri, "artifact", self.day.day_id, self.sequence, self.filename)

    @property
    def data(self):
        "return the actual data contents of the artifact as BytesIO"
        if not self._data:
            with self.file_handle as f:
                self._data = io.BytesIO(f.read())
        return self._data

    @property
    def path(self):
        "return the path to the artifact"
        # this needs access to Gthnk.filetree in order to work
        if self.day.journal.gthnk:
            filetree_artifacts = self.day.journal.gthnk.filetree.artifacts
            return filetree_artifacts.get_path_id(self.day.day_id, self.sequence)

    @property
    def full_filename(self):
        "return the full path to the artifact"
        return os.path.join(self.path, self.filename)

    @property
    def file_handle(self):
        "return the file handle of the artifact"        
        return open(self.full_filename, 'rb')

    def __repr__(self):
        if self._data:
            return f"<Artifact {self.day.day_id}/{self.sequence}/{self.filename} ({self._data.getbuffer().nbytes} bytes)>"
        else:
            return f"<Artifact {self.day.day_id}/{self.sequence}/{self.filename} (lazy)>"
