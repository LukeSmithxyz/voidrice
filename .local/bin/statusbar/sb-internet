#!/bin/sh

# Show wifi 📶 and percent strength or 📡 if none.
# Show 🌐 if connected to ethernet or ❎ if none.
# Show 🔒 if a vpn connection is active

case $BLOCK_BUTTON in
	1) "$TERMINAL" -e nmtui; pkill -RTMIN+4 dwmblocks ;;
	3) notify-send "🌐 Internet module" "\- Click to connect
📡: no wifi connection
📶: wifi connection with quality
❎: no ethernet
🌐: ethernet working
🔒: vpn is active
" ;;
	6) "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

case "$(cat /sys/class/net/w*/operstate 2>/dev/null)" in
	down) wifiicon="📡 " ;;
	up) wifiicon="$(awk '/^\s*w/ { print "📶", int($3 * 100 / 70) "% " }' /proc/net/wireless)" ;;
esac

printf "%s%s%s\n" "$wifiicon" "$(sed "s/down/❎/;s/up/🌐/" /sys/class/net/e*/operstate 2>/dev/null)" "$(sed "s/.*/🔒/" /sys/class/net/tun*/operstate 2>/dev/null)"
