#!/bin/bash

if [ -f $(pgrep offlineimap) ]; then
	offlineimap -o
	echo "Sync begun."
else
	echo "Sync in progress."
fi
