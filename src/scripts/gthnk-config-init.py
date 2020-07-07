#!/usr/bin/env python3

import os
import sys
import click
import random

template = """
# Gthnk Configuration

WEB_JOURNAL_FILE = "{gthnk_path}/journal-web.txt"

INPUT_FILES = "{gthnk_path}/journal-web.txt,{gthnk_path}/journal.txt"
BACKUP_PATH = "{gthnk_path}/backup"
EXPORT_PATH = "{gthnk_path}/export"

SQLALCHEMY_DATABASE_URI = "sqlite:///{gthnk_path}/gthnk.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOG = "{gthnk_path}/gthnk.log"

BASE_URL = "http://gthnk.lan"

LOG_LEVEL = "INFO"
SECRET_KEY = {secret_key}
"""

def write_config_file(out_file, gthnk_path):
    secret_key = str(os.urandom(24))
    with open(out_file, "w") as f:
        f.write(template.format(
            gthnk_path=gthnk_path,
            secret_key=secret_key)
        )

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: gthnk-config.init.py config_filename gthnk_data_path")
        print("ex: gthnk-config.init.py ~/.gthnk/gthnk.conf ~/.gthnk")
        sys.exit(1)
    else:
        out_file = sys.argv[1]
        gthnk_path = sys.argv[2]
        print("write config: {}".format(out_file))
        write_config_file(out_file=out_file, gthnk_path=gthnk_path)
