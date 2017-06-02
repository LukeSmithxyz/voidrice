#!/bin/bash
mfile="$1"
sfile="$2"
windowid="$3"
PID=$(cat $HOME/.config/live-latex-preview/activepid 2> /dev/null)
if [ -e /proc/${PID} -a /proc/${PID}/exe ] ; then
    exit 0
elif [ "$HOME/.config/live-latex-preview/activepid" -nt "$sfile" ] ; then
    exit 0
else
    live-latex-update.sh "$mfile" "$windowid" &>/dev/null &
    echo -n "$!" > "$HOME/.config/live-latex-preview/activepid" 2>/dev/null
fi
exit 0
