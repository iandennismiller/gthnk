#!/bin/bash

if [[ -z $1 ]]; then
    echo "error: configuration filename is required."
    echo "usage: gthnk-config-init.sh FILENAME"
    exit
fi

cat <<EOF > "$1"
PROJECT_NAME = "gthnk"
IP = "0.0.0.0"
PORT = 1620
LOG = "/home/gthnk/storage/gthnk.log"
LOG_LEVEL = "WARN"
SQLALCHEMY_DATABASE_URI = "sqlite:////home/gthnk/storage/gthnk.db"
SECRET_KEY = '\x19h\x83\x11\xef\xdeL\x92\xc2\xa4\xd5T&\xd0\xf1\x87\x91\x9bQ7\xe6\x18A\xea'

BASE_URL = "http://local.gthnk.com"

SECURITY_PASSWORD_SALT = 'O6msWfo5nkV7wIoh'
SECURITY_POST_LOGIN_VIEW = "/admin"
SECURITY_PASSWORD_HASH = 'sha256_crypt'
SECURITY_URL_PREFIX = '/user'
SECURITY_CHANGEABLE = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

DEBUG = False
DEBUG_TOOLBAR = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USERNAME = None
MAIL_PASSWORD = None

CELERY_BROKER_URL = 'sqla+sqlite:///home/gthnk/storage/celery-db.sqlite'
CELERY_RESULT_BACKEND = 'db+sqlite:///home/gthnk/storage/celery-results.sqlite'

BACKUP_PATH = "/home/gthnk/storage/backup"
INPUT_FILES = "/home/gthnk/storage/journal.txt"
PROJECT_PATH = "/home/gthnk/storage/Work"
EXPORT_PATH = "/home/gthnk/storage/export"
EOF
