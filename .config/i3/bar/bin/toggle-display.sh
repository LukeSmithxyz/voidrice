#!/usr/bin/env bash

echo $(dirname $(readlink -f "$0"))

i3bar_update=$(dirname $(readlink -f "$0"))/load-i3-bars.sh

xrandr "$@"

if [ -f $i3bar_update ]; then
	sleep 1
	$i3bar_update
fi
