#!/bin/sh

case $BLOCK_BUTTON in
	1) notify-send "🧠 Memory hogs" "$(ps axch -o cmd,%mem | awk '{cmd[$1]+=$2} END {for (i in cmd) print i, cmd[i]}' | sort -nrk2 | head)" ;;
	2) setsid -f "$TERMINAL" -e htop ;;
	3) notify-send "🧠 Memory module" "\- Shows Memory Used/Total.
- Click to show memory hogs.
- Middle click to open htop." ;;
	6) setsid -f "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

free="$(free --mebi)"
free="${free#*Mem:}"

set -- $free

printf "🧠%2.2fGiB/%2.2fGiB\n" "$(( $2 * 100 / 1024 ))e-2" "$(( $1 * 100 / 1024 ))e-2"
