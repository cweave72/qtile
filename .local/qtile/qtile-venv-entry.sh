#!/bin/bash

# SCRIPTPATH will be set to the path of this script.
SCRIPTPATH=$(dirname $(realpath "${BASH_SOURCE[0]}"))

LOG=qtile-venv-entry.log
touch $LOG

echo "In qtile-venv-entry.sh script" > $LOG
pwd >> $LOG
echo $SCRIPTPATH >> $LOG

function activate_env {
    echo "Activating $1." >> $LOG
    uv sync
    source $1/bin/activate >> $LOG 2>&1
    if [ ! $? -eq 0 ]; then
        echo "Error activating the virtual env." >> $LOG
        exit 1
    fi
}

VENV_DIR=.venv

# Activate the virtual env.
activate_env $SCRIPTPATH/$VENV_DIR
if [ $? -eq 0 ]; then
    echo "Successfully activated venv." >> $LOG
fi

echo "Starting qtile (args=$@)." >> $LOG
which qtile >> $LOG
exec qtile start "$@" >> $LOG
