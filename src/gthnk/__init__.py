import json
from .utils import init_logger


class Gthnk(object):
    def __init__(self, config_filename):
        self.load_config(config_filename)

        if "log_level" in self.config:
            log_level = self.config["log_level"]
        else:
            log_level = "INFO"

        if "log_filename" in self.config:
            self.logger = init_logger(
                name=__name__,
                filename=self.config["log_filename"],
                level=log_level,
            )
        else:
            self.logger = init_logger(name=__name__, level=log_level)

        from .model.journal import Journal
        self.journal = Journal(logger=self.logger)

        self.lazy = True

        # if self.config["backend"] == "filetree":
        self.init_filetree(filetree_root=self.config["filetree_root"])

    def load_config(self, filename):
        "Load the journal configuration."
        with open(filename, "r") as f:
            self.config = json.load(f)

    def init_filetree(self, filetree_root):
        self.logger.info("loading filetree backend")
        from .filetree import FileTree
        self.filetree = FileTree(
            journal=self.journal,
            path=filetree_root,
        )

        # only load all days if lazy is explicitly False
        if "lazy" in self.config and self.config["lazy"] is False:
            self.filetree.load_all_days()
            self.lazy = False
        # default to lazy loading
        else:
            self.filetree.scan_day_ids()

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
