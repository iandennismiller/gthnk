import os
import json

from dotenv import dotenv_values

from .utils import init_logger
from .filebuffer import FileBuffer
from .filetree import FileTreeRoot

try:
    from .llm import LLM
except ModuleNotFoundError:
    LLM = None


class Gthnk(object):
    def __init__(self, config_filename=None):
        if config_filename is None:
            config_filename = ".env"
            self.config = dotenv_values(config_filename)
            if self.config == {}:
                config_filename = os.path.expanduser("~/.config/gthnk/gthnk.conf")
                self.config = dotenv_values(config_filename)
        else:
            self.config = dotenv_values(config_filename)

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

        # self.lazy = True
        self.llm = None

        # if self.config["BACKEND"] == "filetree":
        self.init_filetree(filetree_root=self.config["FILETREE_ROOT"])

    def init_filetree(self, filetree_root):
        self.logger.info(f"Filetree: {filetree_root}")
        self.filetree = FileTreeRoot(
            journal=self.journal,
            path=filetree_root,
        )

        self.filetree.days.load_all()
        self.filetree.artifacts.load_all()

        # # only load all days if lazy is explicitly False
        # if "lazy" in self.config and self.config["LAZY"] is False:
        #     self.filetree.days.load_all()
        #     self.lazy = False
        # # default to lazy loading
        # else:
        #     self.filetree.scan_ids()

    def ask_llm(self, query):
        if LLM and not self.llm:
            self.llm = LLM()
        return self.llm.ask(query)

    def refresh_llm(self):
        if not LLM:
            return
        if not self.llm:
            self.llm = LLM()

        created_count = 0
        exists_count = 0

        for day in self.journal.days.values():
            for entry in day.entries.values():
                created = self.llm.context_db.add(entry)
                if created:
                    created_count += 1
                else:
                    exists_count += 1

        self.logger.info(f"Refreshed entries in LLM context db: created {created_count}, exists {exists_count}")

    def register_buffers(self, buffer_filenames):
        "Register a new buffer with the journal."
        for buffer_filename in buffer_filenames:
            self.logger.info(f"Buffer: {buffer_filename}")
            self.buffers.append(buffer_filename)

    def import_buffers(self):
        "Scan the available buffers for new entries and import them."
        for buffer_filename in self.buffers:
            buffer = FileBuffer(buffer_filename, journal=self.journal)

    def rotate_buffers(self):
        "Tell all of the buffers to rotate their files."
        for buffer_filename in self.buffers:
            buffer = FileBuffer(buffer_filename, journal=self.journal)
            buffer.backup(filetree_root=self.config["FILETREE_ROOT"])
            buffer.clear()
