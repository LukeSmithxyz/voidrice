#!/bin/sh

[ "$(pgrep -x "$(basename "$0")" | wc -l)" -gt 2 ] && exit

while : ; do
	pgrep -x mpd || exit
	mpc idle > /dev/null
	pkill -RTMIN+11 i3blocks ;
done
