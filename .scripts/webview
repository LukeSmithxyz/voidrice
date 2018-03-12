#!/bin/bash

# Feed script a url.
# If an image, it will view in feh,
# if a video or gif, it will view in mpv
# if a music file or pdf, it will download,
# otherwise it opens link in browser.

# List of sites that will be opened in mpv.
vidsites="youtube.com
	\|hooktube.com
	\|bitchute.com
	"
ext="${1##*.}"
mpvFiles="mkv mp4 gif"
fehFiles="png jpg jpeg jpe"
wgetFiles="mp3 flac opus mp3?source=feed pdf"

if echo $fehFiles | grep -w $ext > /dev/null; then
	feh "$1" >/dev/null &
elif echo $mpvFiles | grep -w $ext > /dev/null; then
	mpv --loop --quiet "$1" > /dev/null &
elif echo $wgetFiles | grep -w $ext > /dev/null; then
	wget "$1" >/dev/null &
elif echo "$@" | grep "$vidsites">/dev/null; then
	mpv -quiet "$1" > /dev/null &
else
	$BROWSER "$1" 2>/dev/null & disown
fi
