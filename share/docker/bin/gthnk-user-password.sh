#!/bin/bash

SETTINGS=/home/gthnk/.gthnk/gthnk.conf \
    gthnk change_password -u "$1" -p "$2"
