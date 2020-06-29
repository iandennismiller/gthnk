#!/bin/bash

cd ~/gthnk
SETTINGS=/home/gthnk/storage/gthnk.conf /home/gthnk/venv/bin/manage.py user_add -e "$1" -p "$2"
