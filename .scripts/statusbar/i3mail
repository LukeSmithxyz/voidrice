#!/bin/sh

# i3blocks mail module.
# Displays number of unread mail and an loading icon if updating.
# When clicked, brings up `neomutt`.

case $BLOCK_BUTTON in
	1) "$TERMINAL" -e neomutt ;;
	2) setsid $HOME/.config/mutt/etc/mailsync.sh >/dev/null & ;;
	3) pgrep -x dunst >/dev/null && notify-send "<b>📬 Mail module:</b>
- Shows unread mail
- Shows 🔃 if syncing mail
- Left click opens neomutt
- Middle click syncs mail" ;;
esac

echo "$(du -a ~/.mail/*/INBOX/new/* 2>/dev/null | sed -n '$=')$(cat ~/.config/mutt/.dl 2>/dev/null)"

