#!/bin/bash

GTHNK_PATH=$1

if [ ! -f ${GTHNK_PATH}/gthnk.conf ]; then
    echo "Creating configuration file"
    gthnk-config-init.py ${GTHNK_PATH}/gthnk.conf ${GTHNK_PATH}
fi

if [ ! -f ${GTHNK_PATH}/gthnk.db ]; then
    echo "Creating database"
    gthnk-db-init.sh

    echo "Creating default user"
    gthnk-user-add.sh gthnk gthnk
fi
