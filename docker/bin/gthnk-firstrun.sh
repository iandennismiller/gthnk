#!/bin/bash

if [[ -z $1 ]]; then
    echo "error: configuration filename is required."
    echo "usage: gthnk-firstrun.sh FILENAME"
    exit
fi

~/.local/bin/gthnk-config-init.sh "$1"
~/.local/bin/gthnk-db-init.sh
~/.local/bin/gthnk-user-add.sh user@example.com secret

mkdir -p /home/gthnk/storage/export/attachment \
    /home/gthnk/storage/export/markdown \
    /home/gthnk/storage/export/text \
    /home/gthnk/storage/export/thumbnail \
    /home/gthnk/storage/export/preview
