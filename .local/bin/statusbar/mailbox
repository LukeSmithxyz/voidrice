#!/bin/sh

# Displays number of unread mail and an loading icon if updating.
# When clicked, brings up `neomutt`.

case $BLOCK_BUTTON in
	1) setsid "$TERMINAL" -e neomutt & ;;
	2) setsid mailsync >/dev/null & ;;
	3) notify-send "📬 Mail module" "\- Shows unread mail
- Shows 🔃 if syncing mail
- Left click opens neomutt
- Middle click syncs mail" ;;
	6) "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

unread="$(find "${XDG_DATA_HOME:-$HOME/.local/share}"/mail/*/[Ii][Nn][Bb][Oo][Xx]/new/* -type f | wc -l 2>/dev/null)"

icon="$(cat "/tmp/imapsyncicon_$USER" 2>/dev/null)"

[ "$unread" = "0" ] && [ "$icon" = "" ] || echo "📬 $unread$icon"
