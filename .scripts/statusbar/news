#!/bin/sh

# i3blocks newsboat module.
# Displays number of unread news items and an loading icon if updating.
# When clicked, brings up `newsboat`.

case $BLOCK_BUTTON in
        1) setsid "$TERMINAL" -e newsboat ;;
	2) setsid newsup >/dev/null & exit ;;
        3) pgrep -x dunst >/dev/null && notify-send "<b>📰 News module:</b>
- Shows unread news items
- Shows 🔃 if updating with \`newsup\`
- Left click opens newsboat
- Middle click syncs RSS feeds
<b>Note:</b> Only one instance of newsboat (including updates) may be running at a time." ;;
esac

 cat ~/.config/newsboat/.update 2>/dev/null || echo "$(newsboat -x print-unread | awk '{ print $1}' | sed s/^0$//g)$(cat ~/.config/newsboat/.update 2>/dev/null)"
