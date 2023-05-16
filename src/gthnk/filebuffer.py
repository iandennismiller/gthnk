from .gthnk_format import parse_text
from .model.journal import Journal


class FileBuffer(object):
    """
    A filebuffer is a representation of a journal file on disk.
    If journal is passed as a parameter, the filebuffer will be added to the journal.
    """
    def __init__(self, filename, journal=None):
        self.filename = filename
        if journal is None:
            self.journal = Journal()
        else:
            self.journal = journal
        self.read()
    
    def read(self):
        "Read the file buffer and return a Journal object."
        with open(self.filename, 'r') as f:
            raw_entries = parse_text(f.read())

            for day_id in raw_entries.keys():
                day = self.journal.get_day(day_id)

                for timestamp in raw_entries[day_id].keys():
                    entry = day.get_entry(timestamp)
                    entry.content = raw_entries[day_id][timestamp]

            return self.journal
