import json


class Gthnk(object):
    def __init__(self, config_filename):
        self.load_config(config_filename)

        from .model.journal import Journal
        self.journal = Journal()

        if self.config["backend"] == "filetree":
            self.init_filetree_backend(filetree_root=self.config["filetree_root"])

    def load_config(self, filename):
        "Load the journal configuration."
        with open(filename, "r") as f:
            self.config = json.load(f)

    def init_filetree_backend(self, filetree_root):
        print("loading filetree backend")
        from .filetree import FileTree
        self.backend = FileTree(
            journal=self.journal,
            path=filetree_root,
        )
        self.backend.load_all_days()

    def register_buffer(self, buffer):
        "Register a new buffer with the journal."
        pass

    def import_buffers(self):
        "Scan the available buffers for new entries and import them."
        pass

    def rotate_buffers(self):
        "Tell all of the buffers to rotate their files."
        pass
