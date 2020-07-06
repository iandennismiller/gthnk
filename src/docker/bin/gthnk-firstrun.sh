#!/bin/bash

~/.local/bin/gthnk-config-init.py /home/gthnk/.gthnk/gthnk.conf /home/gthnk/.gthnk
~/.local/bin/gthnk-db-init.sh
~/.local/bin/gthnk-user-add.sh gthnk gthnk
