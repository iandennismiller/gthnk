#!/bin/bash

if [[ -z $1 ]]; then
    echo "error: configuration filename is required."
    echo "usage: gthnk-config-init.sh FILENAME"
    exit
fi

cat <<EOF > "$1"
# Gthnk Configuration

INPUT_FILES = "/home/gthnk/.gthnk/journal.txt"
BACKUP_PATH = "/home/gthnk/.gthnk/backup"
EXPORT_PATH = "/home/gthnk/.gthnk/export"

SQLALCHEMY_DATABASE_URI = "sqlite:////home/gthnk/.gthnk/gthnk.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOG = "/home/gthnk/.gthnk/gthnk.log"

BASE_URL = "http://gthnk.lan"

LOG_LEVEL = "INFO"
SECRET_KEY = '\x19h\x83\x11\xef\xdeL\x92\xc2\xa4\xd5T&\xd0\xf1\x87\x91\x9bQ7\xe6\x18A\xea'
EOF
