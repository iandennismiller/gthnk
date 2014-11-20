#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import Gthnk, logging, flask
import Gthnk.JournalBuffer

def main():
    app = flask.Flask(__name__)
    app.config.from_envvar('SETTINGS')
    Gthnk.db.init_app(app)

    with app.app_context():
        journal_buffer = Gthnk.JournalBuffer.TextFileJournalBuffer()
        journal_buffer.process_list(glob.glob("/Users/idm/Library/Journal/auto/*.txt"))
        journal_buffer.save_entries()

if __name__ == "__main__":
    main()

# import any Journal Buffers that might have entries ready for importing
# first the current Live Journal file.
# also include dropbox files, etc

# create a backup of the file in JOURNAL_PATH/backups
# load and parse the file
# for each entry in the hash buffer, create an Entry in the database
# ... unless one with the same content and same timestamp already exists

# now reset the file size to 0.
