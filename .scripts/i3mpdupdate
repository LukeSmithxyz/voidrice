#!/bin/sh

[ "$(pgrep -x i3mpdupdate | wc -l)" -gt 2 ] && exit

while : ; do
	mpc idle > /dev/null
	pkill -RTMIN+11 i3blocks ;
done
