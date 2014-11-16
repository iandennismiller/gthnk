# -*- coding: utf-8 -*-
# greenthink-library (c) 2013 Ian Dennis Miller

import re, json, datetime, os, shutil
from collections import defaultdict
from .JournalParser import JournalParser

def split_filename_list(filename_str):
    [x.strip() for x in filename_str.split(',')]

class TextFileParser(JournalParser):
    """
    provide functions for loading content from a text file
    """
    def process_file(self, filename):
        with open(filename, "r") as f:
            contents = f.read()
        self.parser.parse(contents)

    def process_file_list(self, filename_list):
        for filename in filename_list:
            self.proces_file(filename)
