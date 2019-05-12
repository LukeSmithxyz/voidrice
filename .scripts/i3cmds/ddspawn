#!/bin/sh

# Toggle floating dropdown terminal in i3, or start if non-existing.
# $1 is	the script run in the terminal.
# All other args are terminal settings.
# Terminal names are in dropdown_* to allow easily setting i3 settings.

[ -z "$1" ] && exit

script=$1
shift
if xwininfo -tree -root | grep "(\"dropdown_$script\" ";
then
	echo "Window detected."
	i3 "[instance=\"dropdown_$script\"] scratchpad show; [instance=\"dropdown_$script\"] move position center"
else
	echo "Window not detected... spawning."
	i3 "exec --no-startup-id $TERMINAL -n dropdown_$script $@ -e $script"
fi
