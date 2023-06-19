import os
import shutil
import datetime

from .syntax import parse_text
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

    def backup(self, filetree_root):
        """
        Backup the file buffer.
        """
        current_day_id = datetime.datetime.now().strftime("%Y-%m-%d")
        current_timestamp = current_time = datetime.datetime.now().strftime("%H%M")
        basename = os.path.basename(self.filename)
        filename = f"{current_day_id}-{current_timestamp}-{basename}"
        backup_filename = os.path.join(filetree_root, "backup", filename)
        # copy the file to the backup directory
        shutil.copyfile(self.filename, backup_filename)

    def clear(self):
        """
        Clear the file buffer.
        """
        with open(self.filename, 'w') as f:
            f.write("")
