#!/bin/sh

# A dmenu prompt to unmount drives.
# Provides you with mounted partitions, select one to unmount.
# Drives mounted at /, /boot and /home will not be options to unmount.

drives="$(lsblk -nrpo "name,type,size,mountpoint,label" | awk -F':' '{gsub(/ /,":")}$4!~/\/boot|\/efi|\/home$|SWAP/&&length($4)>1{printf "%s (%s) %s\n",$4,$3,$5}'; awk '/simple-mtpfs/ { print "📱", $2; }' /etc/mtab)"

chosen="$(echo "$drives" | dmenu -i -p "Unmount which drive?")" || exit 1

case "$chosen" in
	📱*)
		chosen="${chosen#📱 }"
		sudo -A umount -l "$chosen"
		;;
	*)
		chosen="${chosen% (*}"
		sudo -A umount -l "$chosen"
		;;
esac && notify-send "🖥️ Drive unmounted." "$chosen successfully unmounted." ||
	notify-send "🖥️ Drive failed to unmount." "Possibly a permissions or I/O issue."
