#!/bin/sh

# Unmount USB drives or Android phones. Replaces the older `dmenuumount`. Fewer
# prompt and also de-decrypts LUKS drives that are unmounted.

set -e

mounteddroids="$(grep simple-mtpfs /etc/mtab | awk '{print "📱" $2}')"
lsblkoutput="$(lsblk -nrpo "name,type,size,mountpoint")"
mounteddrives="$(echo "$lsblkoutput" | awk '($2=="part"||$2="crypt")&&$4!~/\/boot|\/home$|SWAP/&&length($4)>1{printf "💾%s (%s)\n",$4,$3}')"

allunmountable="$(echo "$mounteddroids
$mounteddrives" | sed "/^$/d;s/ *$//")"
test -n "$allunmountable"

chosen="$(echo "$allunmountable" | dmenu -i -p "Unmount which drive?")"
chosen="${chosen%% *}"
test -n "$chosen"

sudo -A umount -l "/${chosen#*/}"
notify-send "Device unmounted." "$chosen has been unmounted."

# Close the chosen drive if decrypted.
cryptid="$(echo "$lsblkoutput" | grep "/${chosen#*/}$")"
cryptid="${cryptid%% *}"
test -b /dev/mapper/"${cryptid##*/}"
sudo -A cryptsetup close "$cryptid"
notify-send "🔒Device dencryption closed." "Drive is now securely locked again."
