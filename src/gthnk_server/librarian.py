# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import os
import shutil
import datetime

from .models.day import Day
from .models.page import Page
from .journal_buffer import TextFileJournalBuffer, split_filename_list
from gthnk.utils import md, overwrite_if_different, overwrite_if_different_bytes


class Librarian(object):
    def __init__(self, app):
        self.app = app
        self.app.logger.info("librarian: init")

    def rotate_buffers(self):
        # import any Journal Buffers that might have entries ready for importing

        input_files = self.app.config["INPUT_FILES"]
        if "WEB_JOURNAL_FILE" in self.app.config:
            input_files += "," + self.app.config["WEB_JOURNAL_FILE"]

        self.app.logger.debug("processing list: {}".format(input_files))
        file_list = split_filename_list(input_files)

        self.app.logger.info("rotating")

        # create a new backup path
        todays_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H%M%S")
        backup_path = os.path.join(self.app.config["BACKUP_PATH"], todays_date)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        self.app.logger.info("write to backup path: {}".format(backup_path))

        for filename in file_list:
            self.app.logger.info("load and parse: {}".format(filename))
            try:
                shutil.copy2(filename, backup_path)

                # load and parse the file
                journal_buffer = TextFileJournalBuffer()
                journal_buffer.process_one(filename)
                journal_buffer.save_entries()
            except FileNotFoundError:
                pass

            # now reset the file size to 0.
            with open(filename, "w", encoding='utf-8'):
                pass

            self.app.logger.info("finish: {}".format(filename))

    def export_journal(self):
        app = self.app
        app.logger.info("librarian: start export")

        # create export path if necessary
        export_path = app.config["EXPORT_PATH"]
        md(directory=export_path)

        for subdir in ["day", "text", "markdown", "attachment", "thumbnail", "preview"]:
            md(directory=os.path.join(export_path, subdir))

        # export all days
        for day in Day.query.order_by(Day.date).all():
            app.logger.info("export day: {}".format(day))

            # write text representation
            output_filename = os.path.join(app.config["EXPORT_PATH"], "text",
                "{0}.txt".format(day.date))
            app.logger.debug("write text: {}".format(output_filename))
            if not overwrite_if_different(output_filename, day.render()):
                app.logger.debug("skipping; generated file identical to existing export")

            # write markdown representation
            output_filename = os.path.join(app.config["EXPORT_PATH"], "markdown",
                "{0}.md".format(day.date))
            app.logger.debug("write markdown: {}".format(output_filename))
            if not overwrite_if_different(output_filename, day.render_markdown()):
                app.logger.debug("skipping; generated file identical to existing export")

        # export all pages
        for page in Page.query.order_by(Page.id).all():
            app.logger.info("export page: {}".format(page))

            # write raw file
            output_filename = os.path.join(app.config["EXPORT_PATH"], "attachment",
                page.filename())
            app.logger.debug("write raw file: {}".format(output_filename))
            if not overwrite_if_different_bytes(output_filename, page.binary):
                app.logger.debug("skipping; generated file identical to existing export")
            else:
                # write thumbnail
                output_filename = os.path.join(app.config["EXPORT_PATH"], "thumbnail",
                    page.filename(extension="jpg"))
                app.logger.debug("write thumbnail: {}".format(output_filename))
                overwrite_if_different_bytes(output_filename, page.thumbnail)

                # write preview
                output_filename = os.path.join(app.config["EXPORT_PATH"], "preview",
                    page.filename(extension="jpg"))
                app.logger.debug("write preview: {}".format(output_filename))
                overwrite_if_different_bytes(output_filename, page.preview)

        app.logger.info("librarian: finish export")
