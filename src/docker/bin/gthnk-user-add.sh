#!/bin/bash

SETTINGS=/home/gthnk/.local/mnt/shared/gthnk.conf \
    ~/.local/bin/gthnk.py \
    user_add -u "$1" -p "$2"
