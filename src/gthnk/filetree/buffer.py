from __future__ import annotations
from typing import TYPE_CHECKING
import os
import shutil
import datetime

from ..syntax import parse_text

if TYPE_CHECKING:
    from ..model.journal import Journal


class FileBuffer:
    """
    A filebuffer is a representation of a journal file on disk.
    If journal is passed as a parameter, the filebuffer will be added to the journal.
    """
    def __init__(self, filename:str, journal:Journal):
        self.filename = filename
        self.journal = journal

    def read(self):
        "Read the file buffer."
        with open(self.filename, 'r', encoding="utf-8") as file_handle:
            raw_entries = parse_text(file_handle.read())

            for datestamp, raw_day in raw_entries.items():
                day = self.journal.get_day(datestamp)
                if day is None:
                    day = self.journal.create_day(datestamp)

                for timestamp, raw_entry in raw_day.items():
                    entry = day.get_entry(timestamp)
                    if entry is None:
                        day.create_entry(timestamp=timestamp, content=raw_entry)
                    else:
                        # overwrite the content with whatever is in the file buffer
                        entry.content = raw_entry

    def backup(self):
        """
        Backup the file buffer.
        """
        filetree_root = os.path.expanduser(self.journal.gthnk.config["FILETREE_ROOT"])
        current_datestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        current_timestamp = datetime.datetime.now().strftime("%H%M")
        basename = os.path.basename(self.filename)
        filename = f"{current_datestamp}-{current_timestamp}-{basename}"
        backup_filename = os.path.join(filetree_root, "backup", filename)

        # copy the file to the backup directory
        shutil.copyfile(self.filename, backup_filename)

    def clear(self):
        """
        Clear the file buffer.
        """
        with open(self.filename, 'w', encoding="utf-8") as file_handle:
            file_handle.write("")
