#!/bin/sh

# Displays number of upgradeable packages.
# For this to work, have a `pacman -Sy` command run in the background as a
# cronjob every so often as root. This script will then read those packages.
# When clicked, it will run an upgrade via pacman.
#
# Add the following text as a file in /usr/share/libalpm/hooks/statusbar.hook:
#
# [Trigger]
# Operation = Upgrade
# Type = Package
# Target = *
#
# [Action]
# Description = Updating statusbar...
# When = PostTransaction
# Exec = /usr/bin/pkill -RTMIN+8 dwmblocks # Or i3blocks if using i3.

case $BLOCK_BUTTON in
	1) setsid -f "$TERMINAL" -e sb-popupgrade ;;
	2) notify-send "$(/usr/bin/pacman -Qu)" ;;
	3) notify-send "🎁 Upgrade module" "📦: number of upgradable packages
- Left click to upgrade packages
- Middle click to show upgradable packages" ;;
	6) "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

pacman -Qu | grep -Fcv "[ignored]" | sed "s/^/📦/;s/^📦0$//g"
