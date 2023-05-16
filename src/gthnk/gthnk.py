import json

from .model.journal import Journal
from .filetree import FileTree


class Gthnk(object):
    def __init__(self, config_filename):
        self.load_config(config_filename)
        self.journal = Journal()

        if self.config["backend"] == "filetree":
            print("loading filetree backend")
            self.backend = FileTree(
                journal=self.journal,
                path=self.config["filetree_root"],
            )
            self.backend.load_all_days()

    def load_config(self, filename):
        "Load the journal configuration."
        with open(filename, "r") as f:
            self.config = json.load(f)

    def update_filetree(self):
        "Update the filetree with the latest journal state."
        pass

    def register_buffer(self, buffer):
        "Register a new buffer with the journal."
        pass

    def import_buffers(self):
        "Scan the available buffers for new entries and import them."
        pass

    def import_page(self, page):
        "Import a page into the journal."
        pass

    def rotate_buffers(self):
        "Tell all of the buffers to rotate their files."
        pass
    
    def get_entry(self, entry_id):
        "Get an entry by its ID."
        pass

    def get_day(self, day_id):
        "Get a day by its ID."
        pass

    def search_entries(self, query):
        "Search entries for a query."
        pass

    def get_page(self, page_id):
        "Get a page by its ID."
        pass
