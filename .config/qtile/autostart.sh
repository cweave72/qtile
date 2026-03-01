#!/bin/bash
DIR="/usr/bin"

nm-applet &

PICOM_VER=$(picom --version)
PICOM_OPTS=
if [[ "$PICOM_VER" == "v9" ]]; then
    PICOM_OPTS=--experimental-backends
fi
picom --config ~/.config/picom/picom.conf $PICOM_OPTS &
