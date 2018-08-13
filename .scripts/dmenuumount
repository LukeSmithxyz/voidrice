#!/bin/sh
# A dmenu prompt to unmount drives.
# Provides you with mounted partitions, select one to unmount.
# Drives mounted at /, /boot and /home will not be options to unmount.

drives=$(lsblk -nrpo "name,type,size,mountpoint" | awk '$2=="part"&&$4!~/\/boot|\/home$|SWAP/&&length($4)>1{printf "%s (%s) on %s\n",$1,$3,$4}')
[ -z "$drives" ] && exit
chosen=$(echo "$drives" | dmenu -i -p "Unmount which drive?" | awk '{print $1}')
[ -z "$chosen" ] && exit
sudo -A umount "$chosen" && pgrep -x dunst && notify-send "$chosen unmounted."
