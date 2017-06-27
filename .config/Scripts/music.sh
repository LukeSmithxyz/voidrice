#!/bin/bash
if [ -f $(pgrep mpd) ];
	then
	echo "mpd not yet active. Activating."
	mpd && urxvt -e ncmpcpp
	else
	echo "mpd already active."
	urxvt -e ncmpcpp
fi
