#!/bin/sh

case $BLOCK_BUTTON in
	1) notify-send "<b>🧠 Memory hogs:</b>
$(ps axch -o cmd:15,%mem --sort=-%mem | head)" ;;
	3) notify-send "<b>🧠 Memory module:</b>
- Shows Memory Used/Total.
- Click to show memory hogs." ;;
esac

free -h | awk '/^Mem:/ {print $3 "/" $2}'
