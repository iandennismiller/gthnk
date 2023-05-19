import os
from io import BytesIO


class Artifact(object):
    def __init__(self, day, sequence, filename, data:BytesIO=None):
        self.day = day
        self.sequence = sequence
        self.filename = filename
        self._data = data
    
    def get_uri(self):
        return os.path.join(self.day.journal.get_uri(), self.day.day_id, self.sequence, self.filename)

    def set_data(self, data):
        "Set the data contents of the artifact as BytesIO"
        self._data = BytesIO(data)

    @property
    def data(self):
        "return the actual data contents of the artifact as BytesIO"
        return self.bytesio.getvalue()

    @property
    def bytesio(self):
        "return a BytesIO object containing the data contents of the artifact"
        if not self._data:
            with open(self.filename, 'rb') as f:
                self._data = io.BytesIO(f.read())
        return self._data
        description = f"Artifact {self.day}-{self.sequence}"
        return f"[{description}]({self.get_uri()})"
