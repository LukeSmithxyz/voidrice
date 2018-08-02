#!/bin/sh
# Gives a dmenu prompt to mount unmounted drives.
# If they're in /etc/fstab, they'll be mounted automatically.
# Otherwise, you'll be prompted to give a mountpoint from already existsing directories.
# If you input a novel directory, it will prompt you to create that directory.
pgrep -x dmenu && exit
COLS="name,type,size,mountpoint"

drives="$(lsblk -rpo "$COLS" | awk '$2=="part"&&$4==""{printf "%s (%s)\n",$1,$3}')"
[ -z "$drives" ] && exit 1
chosen="$(echo "$drives" | dmenu -i -p "Mount which drive?" | awk '{print $1}')"
[ -z "$chosen" ] && exit 1
sudo -A mount "$chosen" && exit 0
# You may want to change the line below for more suggestions for mounting.
# I.e. you can increase the depth of the search, or add directories.
# This will increase the load time briefly though.
mp="$(find /mnt /media /mount /home -type d -maxdepth 5 2>/dev/null | dmenu -i -p "Type in mount point.")"
[ "$mp" = "" ] && exit 1
if [ ! -d "$mp" ]; then
	mkdiryn=$(printf "No\\nYes" | dmenu -i -p "$mp does not exist. Create it?")
	[ "$mkdiryn" = "Yes" ] && sudo -A mkdir -p "$mp"
fi
sudo -A mount "$chosen" "$mp" && pgrep -x dunst && notify-send "$chosen mounted to $mp."
