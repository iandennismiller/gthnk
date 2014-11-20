#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, shutil
import Gthnk, logging, flask
import Gthnk.Adaptors.JournalBuffer

def main():
    app = flask.Flask(__name__)
    app.config.from_envvar('SETTINGS')
    Gthnk.db.init_app(app)

    # import any Journal Buffers that might have entries ready for importing
    app.logger.info("processing list: {}".format(app.config["INPUT_FILES"]))
    file_list = Gthnk.Adaptors.JournalBuffer.split_filename_list(app.config["INPUT_FILES"])
    with app.app_context():
        for filename in file_list:
            app.logger.info("begin: {}".format(filename))
            # create a backup of the file in JOURNAL_PATH/backups
            shutil.copy2(filename, app.config["BACKUP_PATH"])

            # load and parse the file
            journal_buffer = Gthnk.Adaptors.JournalBuffer.TextFileJournalBuffer()
            journal_buffer.process_one(filename)
            journal_buffer.save_entries()

            # now reset the file size to 0.
            #with open(filename, "w"):
            #    pass

            app.logger.info("finish: {}".format(filename))

if __name__ == "__main__":
    main()


