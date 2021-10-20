#!/bin/sh

# Open a terminal window in the same directory as the currently active window.

PID=$(xprop -id "$(xprop -root | awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print $NF}')" | grep -m 1 PID | cut -d " " -f 3)
PID="$(pstree -lpA "$PID" | tail -n 1 | awk -F'---' '{print $NF}' | sed -re 's/[^0-9]//g')"
cd "$(readlink /proc/"$PID"/cwd)" || return 1
"$TERMINAL"
