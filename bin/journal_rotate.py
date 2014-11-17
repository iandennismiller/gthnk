#!/usr/bin/env python

from Gthnk import app
from Gthnk.Adaptors.TextFile import JournalFile

# import any Journal Buffers that might have entries ready for importing
# first the current Live Journal file.
# also include dropbox files, etc

# create a backup of the file in JOURNAL_PATH/backups
# load and parse the file
# for each entry in the hash buffer, create an Entry in the database
# ... unless one with the same content and same timestamp already exists

# now reset the file size to 0.
