# -*- coding: utf-8 -*-
# gthnk (c) 2014 Ian Dennis Miller
import datetime
import os
import shutil

import Gthnk.Adaptors.JournalBuffer


class Librarian(object):
    def __init__(self, app):
        self.app = app

    def rotate_buffers(self):
        # import any Journal Buffers that might have entries ready for importing
        self.app.logger.info("processing list: {}".format(self.app.config["INPUT_FILES"]))
        file_list = Gthnk.Adaptors.JournalBuffer.split_filename_list(self.app.config["INPUT_FILES"])

        # create a new backup path
        todays_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H%M%S")
        backup_path = os.path.join(self.app.config["BACKUP_PATH"], todays_date)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        for filename in file_list:
            self.app.logger.info("begin: {}".format(filename))
            shutil.copy2(filename, backup_path)

            # load and parse the file
            journal_buffer = Gthnk.Adaptors.JournalBuffer.TextFileJournalBuffer()
            journal_buffer.process_one(filename)
            journal_buffer.save_entries()

            # now reset the file size to 0.
            with open(filename, "w"):
                pass

            self.app.logger.info("finish: {}".format(filename))
