#!/bin/bash
cd $(dirname $0)
inboxes=$(cat inboxes)

bash ~/.config/Scripts/check.sh
while :
do
if [ -f $(pgrep offlineimap) ]; then
	offlineimap -o
	echo "OfflineIMAP sync complete."
	bash check.sh
	notmuch new
else
	echo "OfflineIMAP already running."
fi
sleep 60
done
