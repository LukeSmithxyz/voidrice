#!/bin/bash
# Copyright (C) 2012 Stefan Breunig <stefan+measure-net-speed@mathphys.fsk.uni-heidelberg.de>
# Copyright (C) 2014 kaueraal
# Copyright (C) 2015 Thiago Perrotta <perrotta dot thiago at poli dot ufrj dot br>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Get custom IN and OUT labels if provided by command line arguments
while [[ $# -gt 1 ]]; do
    key="$1"
    case "$key" in 
        -i|--inlabel)
            INLABEL="$2"
            shift;;
        -o|--outlabel)
            OUTLABEL="$2"
            shift;;
    esac
    shift
done

[[ -z $INLABEL ]] && INLABEL="IN "
[[ -z $OUTLABEL ]] && OUTLABEL="OUT "

# Use the provided interface, otherwise the device used for the default route.
if [[ -z $INTERFACE ]] && [[ -n $BLOCK_INSTANCE ]]; then
  INTERFACE=$BLOCK_INSTANCE
elif [[ -z $INTERFACE ]]; then
  INTERFACE=$(ip route | awk '/^default/ { print $5 ; exit }')
fi

# Exit if there is no default route
[[ -z "$INTERFACE" ]] && exit

# Issue #36 compliant.
if ! [ -e "/sys/class/net/${INTERFACE}/operstate" ] || \
    (! [ "$TREAT_UNKNOWN_AS_UP" = "1" ] && 
    ! [ "`cat /sys/class/net/${INTERFACE}/operstate`" = "up" ])
then
    echo "$INTERFACE down"
    echo "$INTERFACE down"
    echo "#FF0000"
    exit 0
fi

# path to store the old results in
path="/dev/shm/$(basename $0)-${INTERFACE}"

# grabbing data for each adapter.
read rx < "/sys/class/net/${INTERFACE}/statistics/rx_bytes"
read tx < "/sys/class/net/${INTERFACE}/statistics/tx_bytes"

# get time
time=$(date +%s)

# write current data if file does not exist. Do not exit, this will cause
# problems if this file is sourced instead of executed as another process.
if ! [[ -f "${path}" ]]; then
  echo "${time} ${rx} ${tx}" > "${path}"
  chmod 0666 "${path}"
fi

# read previous state and update data storage
read old < "${path}"
echo "${time} ${rx} ${tx}" > "${path}"

# parse old data and calc time passed
old=(${old//;/ })
time_diff=$(( $time - ${old[0]} ))

# sanity check: has a positive amount of time passed
[[ "${time_diff}" -gt 0 ]] || exit

# calc bytes transferred, and their rate in byte/s
rx_diff=$(( $rx - ${old[1]} ))
tx_diff=$(( $tx - ${old[2]} ))
rx_rate=$(( $rx_diff / $time_diff ))
tx_rate=$(( $tx_diff / $time_diff ))

# shift by 10 bytes to get KiB/s. If the value is larger than
# 1024^2 = 1048576, then display MiB/s instead

# incoming
echo -n "$INLABEL"
rx_kib=$(( $rx_rate >> 10 ))
if hash bc 2>/dev/null && [[ "$rx_rate" -gt 1048576 ]]; then
  printf '%sM' "`echo "scale=1; $rx_kib / 1024" | bc`"
else
  echo -n "${rx_kib}K"
fi

echo -n " "

# outgoing
echo -n "$OUTLABEL"
tx_kib=$(( $tx_rate >> 10 ))
if hash bc 2>/dev/null && [[ "$tx_rate" -gt 1048576 ]]; then
  printf '%sM' "`echo "scale=1; $tx_kib / 1024" | bc`"
else
  echo -n "${tx_kib}K"
fi
