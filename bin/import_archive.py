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
