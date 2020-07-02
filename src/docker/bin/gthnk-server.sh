#!/bin/bash

SETTINGS=/home/gthnk/.gthnk/gthnk.conf \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=1620 \
    FLASK_APP=gthnk/src/gthnk/server.py \
    flask run
