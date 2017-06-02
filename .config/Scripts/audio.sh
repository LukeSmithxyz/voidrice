#!/bin/bash

#This is the ffmpeg command that the audio shortcut in i3 will run.

#Picks a file name for the output file based on availability:

if [[ -f ~/output.flac ]]
	then
		n=1
		while [[ -f ~/output_$n.flac ]]
		do	
			n=$((n+1))
		done
		filename="output_$n.flac"
	else
		filename="output.flac"
fi

#The actual ffmpeg command:

ffmpeg \
-thread_queue_size 1024 \
 -f alsa -ar 44100 -i hw:1 \
-af "volume=12" \
 -c:v libx264 -r 30 -c:a flac $filename
 #-c:v ffvhuff -r 30 -c:a flac $filename
