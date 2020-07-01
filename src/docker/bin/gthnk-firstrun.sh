#!/bin/bash

if [[ -z $1 ]]; then
    echo "error: configuration filename is required."
    echo "usage: gthnk-firstrun.sh FILENAME"
    exit
fi

mkdir -p \
    /home/gthnk/.local/mnt/shared/export/attachment \
    /home/gthnk/.local/mnt/shared/export/markdown \
    /home/gthnk/.local/mnt/shared/export/text \
    /home/gthnk/.local/mnt/shared/export/thumbnail \
    /home/gthnk/.local/mnt/shared/export/preview

~/.local/bin/gthnk-config-init.sh "$1"
~/.local/bin/gthnk-db-init.sh
~/.local/bin/gthnk-user-add.sh gthnk gthnk
