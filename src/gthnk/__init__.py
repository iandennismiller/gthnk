import os
import json
from typing import List

from dotenv import dotenv_values

from .utils import init_logger
from .filetree import FileTree
from .filetree.buffer import FileBuffer
from .model.journal import Journal


class Gthnk(object):
    def __init__(self, config:dict={}, config_filename:str=""):
        self.journal = Journal(gthnk=self)
        self.init_config(config, config_filename)
        self.init_logging()
        self.init_filetree(filetree_root=self.config["FILETREE_ROOT"])
        self.init_filebuffers()

    def init_config(self, config:dict={}, config_filename:str=""):
        if config is not {}:
            self.config = config
            self.config_filename = "[self.config]"
        elif config_filename is not "":
            self.config = dotenv_values(config_filename)
            self.config_filename = config_filename
        else:
            self.config_filename = ".env"
            self.config = dotenv_values(self.config_filename)
            if self.config == {}:
                self.config_filename = os.path.expanduser("~/.config/gthnk/gthnk.conf")
                self.config = dotenv_values(self.config_filename)

        if self.config == {}:
            raise ValueError(f"Config file not found: {self.config_filename}")

    def init_logging(self):
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
        self.logger.info(f"Load config: {self.config_filename}")

    def init_filebuffers(self):
        "Directly parse a string containing a comma-separated list of input filenames"

        self.buffers:List[str] = []
        if "INPUT_FILES" in self.config:
            self.register_buffers(buffer_filenames=self.config["INPUT_FILES"].split(","))
        else:
            raise ValueError("No INPUT_FILES in config")

    def init_filetree(self, filetree_root:str):
        self.logger.info(f"Filetree: {filetree_root}")
        self.filetree = FileTree(
            journal=self.journal,
            path=filetree_root,
        )
        self.filetree.read_journal()

    def register_buffers(self, buffer_filenames:list):
        "Register a new buffer with the journal."
        for buffer_filename in buffer_filenames:
            self.logger.info(f"Buffer: {buffer_filename}")
            self.buffers.append(buffer_filename)

    def update_filetree(self):
        "Write a day to the filesystem."
        self.filetree.write_journal()

    def rotate_buffers(self):
        "Import all buffers and rotate them."

        for buffer_filename in self.buffers:
            FileBuffer(buffer_filename, journal=self.journal).read()

        # now write the journal to the filesystem
        self.update_filetree()

        # backup the buffers and clear them
        for buffer_filename in self.buffers:
            FileBuffer(buffer_filename, journal=self.journal).backup()

        for buffer_filename in self.buffers:
            FileBuffer(buffer_filename, journal=self.journal).clear()
