#!/bin/sh

# Gets your public ip address checks which country you are in and
# displays that information in the statusbar
#
# https://www.maketecheasier.com/ip-address-geolocation-lookups-linux/
ifinstalled "geoiplookup" || exit
addr="$(curl ifconfig.me 2>/dev/null)" || exit
grep "flag: " ~/.config/emoji | grep "$(geoiplookup $addr | sed 's/.*, //')" | sed "s/flag: //;s/;.*//"
