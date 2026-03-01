# THis should be sourced from .bashrc.

QTILE_VENV=$HOME/.local/qtile/.venv
PY=python3.11

# Use powerline-status (installed in qtile venv)
POWERLINE_BINDINGS=$QTILE_VENV/lib/$PY/site-packages/powerline/bindings/bash

if [[ -n "$SSH_CLIENT" ]]; then
    export POWERLINE_CONFIG_OVERRIDES='ext.shell.colorscheme=default'
fi

if [ -f $POWERLINE_BINDINGS/powerline.sh ]; then
    powerline-daemon -q
    POWERLINE_BASH_CONTINUATION=1
    POWERLINE_BASH_SELECT=1
    source $POWERLINE_BINDINGS/powerline.sh
fi
