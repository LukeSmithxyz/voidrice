#!/bin/sh

# A dmenu prompt to unmount drives.
# Provides you with mounted partitions, select one to unmount.
# Drives mounted at /, /boot and /home will not be options to unmount.

unmountusb() {
	[ -z "$drives" ] && exit
	chosen="$(echo "$drives" | dmenu -i -p "Unmount which drive?")" || exit 1
	chosen="$(echo "$chosen" | awk '{print $1}')"
	[ -z "$chosen" ] && exit
	sudo -A umount "$chosen" && notify-send "💻 USB unmounting" "$chosen unmounted."
	}

unmountandroid() { \
	chosen="$(awk '/simple-mtpfs/ {print $2}' /etc/mtab | dmenu -i -p "Unmount which device?")" || exit 1
	[ -z "$chosen" ] && exit
	sudo -A umount -l "$chosen" && notify-send "🤖 Android unmounting" "$chosen unmounted."
	}

asktype() { \
	choice="$(printf "USB\\nAndroid" | dmenu -i -p "Unmount a USB drive or Android device?")" || exit 1
	case "$choice" in
		USB) unmountusb ;;
		Android) unmountandroid ;;
	esac
	}

drives=$(lsblk -nrpo "name,type,size,mountpoint,label" | awk -F':' '{gsub(/ /,":")}$4!~/\/boot|\/efi|\/home$|SWAP/&&length($4)>1{printf "%s (%s) %s\n",$4,$3,$5}')

if ! grep simple-mtpfs /etc/mtab; then
	[ -z "$drives" ] && echo "No drives to unmount." &&  exit
	echo "Unmountable USB drive detected."
	unmountusb
else
	if [ -z "$drives" ]
	then
		echo "Unmountable Android device detected."
	       	unmountandroid
	else
		echo "Unmountable USB drive(s) and Android device(s) detected."
		asktype
	fi
fi
