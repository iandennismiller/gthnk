import os
import json

from dotenv import dotenv_values

from .utils import init_logger
from .filebuffer import FileBuffer
from .filetree import FileTreeRoot


class Gthnk(object):
    def __init__(self, config=None, config_filename=None):
        if config is not None:
            self.config = config
            config_filename = "[self.config]"
        elif config_filename is not None:
            self.config = dotenv_values(config_filename)
        else:
            config_filename = ".env"
            self.config = dotenv_values(config_filename)
            if self.config == {}:
                config_filename = os.path.expanduser("~/.config/gthnk/gthnk.conf")
                self.config = dotenv_values(config_filename)
        if self.config == {}:
            raise ValueError(f"Config file not found: {config_filename}")

        if "LOG_LEVEL" in self.config:
            log_level = self.config["LOG_LEVEL"]
        else:
            log_level = "INFO"

        if "LOG_FILENAME" in self.config:
            self.logger = init_logger(
                name="gthnk",
                filename=self.config["LOG_FILENAME"],
                level=log_level,
            )
        else:
            self.logger = init_logger(
                name=__name__,
                level=log_level
            )
        self.logger.info("[bold yellow]Start Gthnk[/bold yellow]")
        self.logger.info(f"Load config: {config_filename}")

        self.buffers = []
        if "INPUT_FILES" in self.config:
            self.register_buffers(buffer_filenames=self.config["INPUT_FILES"].split(","))
        else:
            raise ValueError("No INPUT_FILES in config")

        from .model.journal import Journal
        self.journal = Journal(gthnk=self)

        # if self.config["BACKEND"] == "filetree":
        self.init_filetree(filetree_root=self.config["FILETREE_ROOT"])

    def init_filetree(self, filetree_root):
        self.logger.info(f"Filetree: {filetree_root}")
        self.filetree = FileTreeRoot(
            journal=self.journal,
            path=filetree_root,
        )

        self.filetree.days.load_all()

        # # only load all days if lazy is explicitly False
        # if "lazy" in self.config and self.config["LAZY"] is False:
        #     self.filetree.days.load_all()
        #     self.lazy = False
        # # default to lazy loading
        # else:
        #     self.filetree.scan_ids()

    def register_buffers(self, buffer_filenames):
        "Register a new buffer with the journal."
        for buffer_filename in buffer_filenames:
            self.logger.info(f"Buffer: {buffer_filename}")
            self.buffers.append(buffer_filename)

    def update_filetree(self):
        "Write a day to the filesystem."
        self.filetree.write_journal()

    def import_buffers(self):
        "Scan the available buffers for new entries and import them."
        for buffer_filename in self.buffers:
            FileBuffer(buffer_filename, journal=self.journal).read()
        self.update_filetree()

    def rotate_buffers(self):
        "Tell all of the buffers to rotate their files."
        self.import_buffers()

        for buffer_filename in self.buffers:
            buffer = FileBuffer(buffer_filename, journal=self.journal)
            buffer.backup()

        for buffer_filename in self.buffers:
            buffer = FileBuffer(buffer_filename, journal=self.journal)
            buffer.clear()
