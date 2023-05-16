import json
from .utils import init_logger
from dotenv import dotenv_values


class Gthnk(object):
    def __init__(self, config_filename=None):
        if config_filename is None:
            config_filename = ".env"
            self.config = dotenv_values(config_filename)
            if self.config == {}:
                config_filename = os.path.expanduser("~/.config/gthnk/.env")
                self.config = dotenv_values(config_filename)
        else:
            self.config = dotenv_values(config_filename)

        if "log_level" in self.config:
            log_level = self.config["LOG_LEVEL"]
        else:
            log_level = "INFO"

        if "log_filename" in self.config:
            self.logger = init_logger(
                name=__name__,
                filename=self.config["LOG_FILENAME"],
                level=log_level,
            )
        else:
            self.logger = init_logger(name=__name__, level=log_level)
        self.logger.info("Start Gthnk")
        self.logger.info(f"Load config: {config_filename}")

        from .model.journal import Journal
        self.journal = Journal(logger=self.logger)

        # self.lazy = True

        # if self.config["BACKEND"] == "filetree":
        self.init_filetree(filetree_root=self.config["FILETREE_ROOT"])

    def init_filetree(self, filetree_root):
        self.logger.info(f"Filetree backend: {filetree_root}")
        from .filetree import FileTree
        self.filetree = FileTree(
            journal=self.journal,
            path=filetree_root,
        )

        self.filetree.load_all_days()

        # # only load all days if lazy is explicitly False
        # if "lazy" in self.config and self.config["LAZY"] is False:
        #     self.filetree.load_all_days()
        #     self.lazy = False
        # # default to lazy loading
        # else:
        #     self.filetree.scan_day_ids()

    def register_buffer(self, buffer):
        "Register a new buffer with the journal."
        pass

    def import_buffers(self):
        "Scan the available buffers for new entries and import them."
        # fb = FileBuffer("/Users/idm/Work/gthnk/src/tests/data/2012-10-04.txt", journal=j)
        pass

    def rotate_buffers(self):
        "Tell all of the buffers to rotate their files."
        pass
