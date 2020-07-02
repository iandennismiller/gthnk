#!/bin/bash

if [[ -z $1 ]]; then
    echo "error: configuration filename is required."
    echo "usage: gthnk-firstrun.sh FILENAME"
    exit
fi

mkdir -p \
    /home/gthnk/.gthnk/export/attachment \
    /home/gthnk/.gthnk/export/markdown \
    /home/gthnk/.gthnk/export/text \
    /home/gthnk/.gthnk/export/thumbnail \
    /home/gthnk/.gthnk/export/preview

~/.local/bin/gthnk-config-init.sh "$1"
~/.local/bin/gthnk-db-init.sh
~/.local/bin/gthnk-user-add.sh gthnk gthnk
