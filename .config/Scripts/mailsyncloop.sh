#!/bin/bash
offlineimap -o
while :
do
if [ -f $(pgrep offlineimap) ]; then
	offlineimap -o
	echo "OfflineIMAP sync complete."
else
	echo "OfflineIMAP already running."
fi
sleep 60
done
