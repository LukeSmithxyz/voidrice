#!/bin/bash

#This is the ffmpeg command that the screencast shortcut in i3 will run.

#Picks a file name for the output file based on availability:

while [[ -f $HOME/audio$n.flac ]]
do
	n=$((n+1))
done
filename="$HOME/audio$n.flac"

#The actual ffmpeg command:

ffmpeg -y \
 -f alsa -ar 44100 -i hw:1 \
 $filename

