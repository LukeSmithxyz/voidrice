#!/bin/sh

# This loop will update the mpd statusbar module whenever a command changes the
# music player's status. mpd must be running on X's start for this to work.

while : ; do
	mpc idle >/dev/null && kill -45 "$(pidof "${STATUSBAR:-dwmblocks}")" || break
done
