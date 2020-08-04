#!/bin/sh

clock=$(date '+%I')

case "$clock" in
	"00") icon="🕛" ;;
	"01") icon="🕐" ;;
	"02") icon="🕑" ;;
	"03") icon="🕒" ;;
	"04") icon="🕓" ;;
	"05") icon="🕔" ;;
	"06") icon="🕕" ;;
	"07") icon="🕖" ;;
	"08") icon="🕗" ;;
	"09") icon="🕘" ;;
	"10") icon="🕙" ;;
	"11") icon="🕚" ;;
	"12") icon="🕛" ;;
esac

case $BLOCK_BUTTON in
	1) notify-send "This Month" "$(cal --color=always | sed "s/..7m/<b><span color=\"red\">/;s/..27m/<\/span><\/b>/")" && notify-send "Appointments" "$(calcurse -d3)" ;;
	2) setsid -f "$TERMINAL" -e calcurse ;;
	3) notify-send "📅 Time/date module" "\- Left click to show upcoming appointments for the next three days via \`calcurse -d3\` and show the month via \`cal\`
- Middle click opens calcurse if installed" ;;
	6) "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

date "+%Y %b %d (%a) $icon%I:%M%p"
