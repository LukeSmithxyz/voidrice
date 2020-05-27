#!/bin/sh

err() { echo "Usage:
	tag [OPTIONS] file
Options:
	-a: artist/author
	-t: song/chapter title
	-A: album/book title
	-n: track/chapter number
	-N: total number of tracks/chapters
	-d: year of publication
	-g: genre
	-c: comment
You will be prompted for title, artist, album and track if not given." && exit 1 ;}

while getopts "a:t:A:n:N:d:g:c:f:" o; do case "${o}" in
	a) artist="${OPTARG}" ;;
	t) title="${OPTARG}" ;;
	A) album="${OPTARG}" ;;
	n) track="${OPTARG}" ;;
	N) total="${OPTARG}" ;;
	d) date="${OPTARG}" ;;
	g) genre="${OPTARG}" ;;
	c) comment="${OPTARG}" ;;
	f) file="${OPTARG}" ;;
	*) printf "Invalid option: -%s\\n" "$OPTARG" && err ;;
esac done

shift $((OPTIND - 1))

file="$1"

[ ! -f "$file" ] && echo "Provide file to tag." && err

[ -z "$title" ] && echo "Enter a title." && read -r title
[ -z "$artist" ] && echo "Enter an artist." && read -r artist
[ -z "$album" ] && echo "Enter an album." && read -r album
[ -z "$track" ] && echo "Enter a track number." && read -r track

case "$file" in
	*.ogg) echo "Title=$title
Artist=$artist
Album=$album
Track=$track
Total=$total
Date=$date
Genre=$genre
Comment=$comment" | vorbiscomment -w "$file" ;;
	*.opus) echo "Title=$title
Artist=$artist
Album=$album
Track=$track
Total=$total
Date=$date
Genre=$genre
Comment=$comment" | opustags -i -S "$file" ;;
	*.mp3) eyeD3 -Q --remove-all -a "$artist" -A "$album" -t "$title" -n "$track" -N "$total" -Y "$date" "$file" ;;
	*) echo "File type not implemented yet." ;;
esac
