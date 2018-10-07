#!/bin/bash

case $BLOCK_BUTTON in
	1) $TERMINAL -e sudo -A wifi-menu ;;
esac

INTERFACE="${BLOCK_INSTANCE:-wlan0}"

[[ "$(cat /sys/class/net/$INTERFACE/operstate)" = 'down' ]] && echo 📡 && exit

QUALITY=$(grep $INTERFACE /proc/net/wireless | awk '{ print int($3 * 100 / 70 - 1) }')

echo 📶 $QUALITY%
echo 📶 $QUALITY%

# color
if [[ $QUALITY -ge 80 ]]; then
	echo "#00FF00"
elif [[ $QUALITY -lt 40 ]]; then
	echo "#FF0000"
elif [[ $QUALITY -lt 60 ]]; then
	echo "#FF8000"
elif [[ $QUALITY -lt 80 ]]; then
	echo "#FFF600"
fi
