#!/bin/sh

filter() {
	sed "/^volume:/d" | tac | sed -e "s/\\&/&amp;/g;s/\\[paused\\].*/<span color=\"gray\" font_style=\"italic\">/g;s/\\[playing\\].*/<span>/g" | tr -d '\n' | sed -e "s/$/<\\/span>/g"
	}

case $BLOCK_BUTTON in
    1) mpc status | filter && setsid "$TERMINAL" -e ncmpcpp & ;;  # right click, pause/unpause
    2) mpc toggle | filter ;;  # right click, pause/unpause
    3) mpc status | filter && pgrep -x dunst >/dev/null && notify-send "<b>🎵 Music module:</b>
- Shows mpd song playing.
- Italic when paused.
- Left click opens ncmpcpp.
- Middle click pauses.
- Scroll changes track.";;  # right click, pause/unpause
    4) mpc prev   | filter ;;  # scroll up, previous
    5) mpc next   | filter ;;  # scroll down, next
    *) mpc status | filter ;;
esac
