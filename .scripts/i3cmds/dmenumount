#!/bin/sh
# Gives a dmenu prompt to mount unmounted drives.
# If they're in /etc/fstab, they'll be mounted automatically.
# Otherwise, you'll be prompted to give a mountpoint from already existsing directories.
# If you input a novel directory, it will prompt you to create that directory.
pgrep -x dmenu && exit

getmount() { \
	[ -z "$chosen" ] && exit 1
	mp="$(find $1 | dmenu -i -p "Type in mount point.")"
	[ "$mp" = "" ] && exit 1
	if [ ! -d "$mp" ]; then
		mkdiryn=$(printf "No\\nYes" | dmenu -i -p "$mp does not exist. Create it?")
		[ "$mkdiryn" = "Yes" ] && (mkdir -p "$mp" || sudo -A mkdir -p "$mp")
	fi
	}

mountusb() { \
	chosen="$(echo "$usbdrives" | dmenu -i -p "Mount which drive?" | awk '{print $1}')"
	sudo -A mount "$chosen" && notify-send "$chosen mounted." && exit 0
	getmount "/mnt /media /mount /home -maxdepth 5 -type d"
	sudo -A mount "$chosen" "$mp" && notify-send "$chosen mounted to $mp."
	}

mountandroid() { \
	chosen=$(echo "$anddrives" | dmenu -i -p "Which Android device?" | cut -d : -f 1)
	getmount "$HOME -maxdepth 3 -type d"
	simple-mtpfs --device "$chosen" "$mp"
	notify-send "Android device mounted to $mp."
	}

asktype() { \
	case $(printf "USB\\nAndroid" | dmenu -i -p "Mount a USB drive or Android device?") in
		USB) mountusb ;;
		Android) mountandroid ;;
	esac
	}

anddrives=$(simple-mtpfs -l 2>/dev/null)
usbdrives="$(lsblk -rpo "name,type,size,mountpoint" | awk '$2=="part"&&$4==""{printf "%s (%s)\n",$1,$3}')"

if [ -z "$usbdrives" ]; then
	[ -z "$anddrives" ] && echo "No USB drive or Android device detected" && exit
	echo "Android device(s) detected."
	mountandroid
else
	if [ -z "$anddrives" ]; then
		echo "USB drive(s) detected."
	       	mountusb
	else
		echo "Mountable USB drive(s) and Android device(s) detected."
		asktype
	fi
fi
