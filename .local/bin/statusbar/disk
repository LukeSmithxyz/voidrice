#!/bin/sh

# Status bar module for disk space
# $1 should be drive mountpoint, otherwise assumed /.

location=${1:-/}

[ -d "$location" ] || exit

case $BLOCK_BUTTON in
	1) notify-send "💽 Disk space" "$(df -h --output=target,used,size)" ;;
	3) notify-send "💽 Disk module" "\- Shows used hard drive space.
- Click to show all disk info." ;;
	6) "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

case "$location" in
	"/home"* ) icon="🏠" ;;
	"/mnt"* ) icon="💾" ;;
	*) icon="🖥";;
esac

printf "%s: %s\n" "$icon" "$(df -h "$location" | awk ' /[0-9]/ {print $3 "/" $2}')"
