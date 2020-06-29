#!/bin/bash

cd ~/gthnk
SETTINGS=/home/gthnk/storage/gthnk.conf /home/gthnk/venv/bin/manage.py user_del -e "$1"
