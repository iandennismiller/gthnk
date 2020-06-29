# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import datetime
import os
import shutil
import hashlib

import gthnk.adaptors.journal_buffer
from gthnk.models import Day, Page


def overwrite_if_different(filename, new_content):
    # see whether the file exists
    if os.path.isfile(filename):
        # if so, gather the md5 checksums
        with open(filename, "r", encoding='utf-8') as f:
            existing_checksum = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        generated_checksum = hashlib.md5(new_content.encode('utf-8')).hexdigest()

        # compare to md5 checksum of generated file.
        # if different, then overwrite.
        if generated_checksum == existing_checksum:
            return False

    with open(filename, "wb") as f:
        f.write(new_content.encode('utf-8'))
    return True

def overwrite_if_different_bytes(filename, new_content):
    # see whether the file exists
    if os.path.isfile(filename):
        # if so, gather the md5 checksums
        with open(filename, "rb") as f:
            existing_checksum = hashlib.md5(f.read()).hexdigest()
        generated_checksum = hashlib.md5(new_content).hexdigest()

        # compare to md5 checksum of generated file.
        # if different, then overwrite.
        if generated_checksum == existing_checksum:
            return False

    with open(filename, "wb") as f:
        f.write(new_content)
    return True



class Librarian(object):
    def __init__(self, app):
        self.app = app
        self.app.logger.info("librarian: init")

    def rotate_buffers(self):
        # import any Journal Buffers that might have entries ready for importing
        self.app.logger.debug("processing list: {}".format(self.app.config["INPUT_FILES"]))
        file_list = gthnk.adaptors.journal_buffer.split_filename_list(self.app.config["INPUT_FILES"])

        # create a new backup path
        todays_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H%M%S")
        backup_path = os.path.join(self.app.config["BACKUP_PATH"], todays_date)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        for filename in file_list:
            self.app.logger.debug("begin: {}".format(filename))
            shutil.copy2(filename, backup_path)

            # load and parse the file
            journal_buffer = gthnk.adaptors.journal_buffer.TextFileJournalBuffer()
            journal_buffer.process_one(filename)
            journal_buffer.save_entries()

            # now reset the file size to 0.
            with open(filename, "w", encoding='utf-8'):
                pass

            self.app.logger.debug("finish: {}".format(filename))

    def export_journal(self):
        app = self.app
        app.logger.info("librarian: start export")

        # create export path if necessary
        if not os.path.exists(app.config["EXPORT_PATH"]):
            os.makedirs(app.config["EXPORT_PATH"])
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "day"))
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "text"))
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "markdown"))
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "attachment"))
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "thumbnail"))
            os.makedirs(os.path.join(app.config["EXPORT_PATH"], "preview"))

        # export all days
        for day in Day.query.order_by(Day.date).all():
            app.logger.debug(day)

            # write text representation
            output_filename = os.path.join(app.config["EXPORT_PATH"], "text",
                "{0}.txt".format(day.date))
            if not overwrite_if_different(output_filename, day.render()):
                app.logger.debug("skipping; generated file identical to existing export")

            # write markdown representation
            output_filename = os.path.join(app.config["EXPORT_PATH"], "markdown",
                "{0}.md".format(day.date))
            if not overwrite_if_different(output_filename, day.render_markdown()):
                app.logger.debug("skipping; generated file identical to existing export")

        # export all pages
        for page in Page.query.order_by(Page.id).all():
            app.logger.debug(page)

            # write raw file
            output_filename = os.path.join(app.config["EXPORT_PATH"], "attachment",
                page.filename())
            if not overwrite_if_different_bytes(output_filename, page.binary):
                app.logger.debug("skipping; generated file identical to existing export")
            else:
                # write thumbnail
                output_filename = os.path.join(app.config["EXPORT_PATH"], "thumbnail",
                    page.filename(extension="jpg"))
                overwrite_if_different_bytes(output_filename, page.thumbnail)

                # write preview
                output_filename = os.path.join(app.config["EXPORT_PATH"], "preview",
                    page.filename(extension="jpg"))
                overwrite_if_different_bytes(output_filename, page.preview)

        app.logger.info("librarian: finish export")
