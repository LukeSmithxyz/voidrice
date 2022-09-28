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

while getopts "a:t:A:n:N:d:g:c:" o; do case "${o}" in
	a) artist="${OPTARG}" ;;
	t) title="${OPTARG}" ;;
	A) album="${OPTARG}" ;;
	n) track="${OPTARG}" ;;
	N) total="${OPTARG}" ;;
	d) date="${OPTARG}" ;;
	g) genre="${OPTARG}" ;;
	c) comment="${OPTARG}" ;;
	*) printf "Invalid option: -%s\\n" "$OPTARG" && err ;;
esac done

shift $((OPTIND - 1))

file="$1"

temp="$(mktemp -p "$(dirname "$file")")"
trap 'rm -f $temp' HUP INT QUIT TERM PWR EXIT

[ ! -f "$file" ] && echo 'Provide file to tag.' && err

[ -z "$title" ] && echo 'Enter a title.' && read -r title
[ -z "$artist" ] && echo 'Enter an artist.' && read -r artist
[ -z "$album" ] && echo 'Enter an album.' && read -r album
[ -z "$track" ] && echo 'Enter a track number.' && read -r track

cp -f "$file" "$temp" && ffmpeg -i "$temp" -map 0 -y -codec copy \
	-metadata title="$title" \
	-metadata album="$album" \
	-metadata artist="$artist" \
	-metadata track="${track}${total:+/"$total"}" \
	${date:+-metadata date="$date"} \
	${genre:+-metadata genre="$genre"} \
	${comment:+-metadata comment="$comment"} "$file"
