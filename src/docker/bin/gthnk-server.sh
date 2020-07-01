#!/bin/bash

# cd ~/gthnk/src/gthnk

SETTINGS=/home/gthnk/.local/mnt/shared/gthnk.conf \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=1620 \
    FLASK_APP=gthnk/src/gthnk/server.py \
    ~/.local/bin/flask run
