#!/bin/sh

date '+%Y %b %d (%a) %I:%M%p'

case $BLOCK_BUTTON in
	1) pgrep -x dunst >/dev/null && notify-send "$(cal --color=always | sed "s/..7m/<b><span color=\"red\">/;s/..27m/<\/span><\/b>/")" && notify-send "$(calcurse -d3)" ;;
	2) "$TERMINAL" -e calcurse ;;
	3) pgrep -x dunst >/dev/null && notify-send "<b>📅 Time/date module:</b>
- Left click to show upcoming appointments for the next three days via \`calcurse -d3\` and show the month via \`cal\`
- Middle click opens calcurse if installed" ;;
esac
