#!/bin/sh

# Show wifi 📶 and percent strength or 📡 if none.
# Show 🌐 if connected to ethernet or ❎ if none.
# Show 🔒 if a vpn connection is active

case $BLOCK_BUTTON in
	1) "$TERMINAL" -e nmtui; pkill -RTMIN+4 dwmblocks ;;
	3) notify-send "🌐 Internet module" "\- Click to connect
❌: wifi disabled
📡: no wifi connection
📶: wifi connection with quality
❎: no ethernet
🌐: ethernet working
🔒: vpn is active
" ;;
	6) setsid -f "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

# Wifi
if [ "$(cat /sys/class/net/w*/operstate 2>/dev/null)" = 'up' ] ; then
	wifiicon="$(awk '/^\s*w/ { print "📶", int($3 * 100 / 70) "% " }' /proc/net/wireless)"
elif [ "$(cat /sys/class/net/w*/operstate 2>/dev/null)" = 'down' ] ; then
	[ "$(cat /sys/class/net/w*/flags 2>/dev/null)" = '0x1003' ] && wifiicon="📡 " || wifiicon="❌ "
fi

# Ethernet
[ "$(cat /sys/class/net/e*/operstate 2>/dev/null)" = 'up' ] && ethericon="🌐" || ethericon="❎"

# TUN
[ -n "$(cat /sys/class/net/tun*/operstate 2>/dev/null)" ] && tunicon=" 🔒"

printf "%s%s%s\n" "$wifiicon" "$ethericon" "$tunicon"
