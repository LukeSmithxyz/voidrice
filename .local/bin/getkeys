#!/bin/sh

cat "${XDG_DATA_HOME:-$HOME/.local/share}"/larbs/getkeys/"$1" 2>/dev/null && exit
echo "Run command with one of the following arguments for info about that program:"
ls "${XDG_DATA_HOME:-$HOME/.local/share}"/larbs/getkeys
