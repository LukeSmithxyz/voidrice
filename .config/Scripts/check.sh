#!/bin/bash
notification="i3 exec mpv ~/.config/Scripts/ding.opus"

cd $(dirname $0)
while read entry
	do
	[ "$(ls -A $entry)" ] && echo "New mail found in $entry." && exec $notification && notmuch new || echo "No new mail found in $entry."
	done < inboxes
