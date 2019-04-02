#!/bin/sh

case $BLOCK_BUTTON in
	1) setsid "$TERMINAL" -e pulsemixer & ;;
	2) pulsemixer --toggle-mute ;;
	4) pulsemixer --change-volume +5 ;;
	5) pulsemixer --change-volume -5 ;;
	3) pgrep -x dunst >/dev/null && notify-send "📢 Volume module" "\- Shows volume 🔊, 🔇 if muted.
- Middle click to mute.
- Scroll to change."
esac

[ "$(pulsemixer --get-mute)" = "1" ] && printf "🔇\\n" && exit

vol=$(pulsemixer --get-volume | awk '{print $1}')

if [ "$vol" -gt "70" ]; then
	icon="🔊"
elif [ "$vol" -lt "30" ]; then
	icon="🔈"
else
	icon="🔉"
fi

printf "%s %s%%\\n" "$icon" "$vol"
