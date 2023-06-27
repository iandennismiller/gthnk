import os
import sys
from typing import List

from dotenv import dotenv_values

from .utils import init_logger
from .filetree import FileTree
from .filetree.buffer import FileBuffer
from .model.journal import Journal


class Gthnk:
    """
    Gthnk is the main class for the Gthnk application.
    It combines a journal with a file tree.
    """

    def __init__(self, config:dict={}, config_filename:str=""): # pylint: disable=dangerous-default-value
        self.journal = Journal(gthnk=self)
        self.init_config(config, config_filename)
        self.init_logging()
        self.init_filetree()
        self.init_filebuffers()

    def init_config(self, config:dict={}, config_filename:str=""): # pylint: disable=dangerous-default-value
        "Initialize the configuration."
        if config != {}:
            self.config_filename = "Dict()"
            self.config = config
        elif config_filename != "":
            self.config_filename = config_filename
            self.config = dotenv_values(config_filename)
        elif "GTHNK_CONFIG" in os.environ:
            self.config_filename = os.environ["GTHNK_CONFIG"]
            self.config = dotenv_values(self.config_filename)
        else:
            self.config_filename = os.path.expanduser("~/.config/gthnk/gthnk.conf")
            self.config = dotenv_values(self.config_filename)

        if self.config == {}:
            print(f"Config could not be loaded: {self.config_filename}")
            sys.exit(1)

    def init_logging(self):
        "Initialize logging."
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
        self.logger.info("Load config: %s", self.config_filename)

    def init_filebuffers(self):
        "Directly parse a string containing a comma-separated list of input filenames"

        self.buffers:List[str] = []
        if "INPUT_FILES" in self.config:
            buffer_filenames = self.config["INPUT_FILES"].split(",")
            for buffer_filename in buffer_filenames:
                self.logger.info("Buffer: %s", buffer_filename)
                self.buffers.append(buffer_filename)
        else:
            raise ValueError("No INPUT_FILES in config")

    def init_filetree(self):
        "Initialize the filetree."

        if "FILETREE_ROOT" in self.config:
            filetree_root = self.config["FILETREE_ROOT"]
            self.logger.info("Filetree: %s", filetree_root)
            self.filetree = FileTree(
                journal=self.journal,
                path=filetree_root,
            )
            self.filetree.read_journal()
        else:
            raise ValueError("No FILETREE_ROOT in config")

    def rotate_buffers(self):
        "Import all buffers, back them up, and clear them for the next day."

        for buffer_filename in self.buffers:
            FileBuffer(buffer_filename, journal=self.journal).read()

        # write the journal to the filetree
        self.filetree.write_journal()

        # backup the buffers and clear them
        for buffer_filename in self.buffers:
            FileBuffer(buffer_filename, journal=self.journal).backup()

        for buffer_filename in self.buffers:
            FileBuffer(buffer_filename, journal=self.journal).clear()
