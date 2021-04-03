#!/usr/bin/sh

usage ()
{
    printf "Usage : noisereduce <input video file> <output video file>\n"
    exit
}

# Tests for requirements
ifinstalled ffmpeg || { echo >&2 "We require 'ffmpeg' but it's not installed."; exit 1; }
ifinstalled sox || { echo >&2 "We require 'ffmpeg' but it's not installed."; exit 1; }

if [ "$#" -ne 2 ]
then
  usage
fi

if [ ! -e "$1" ]
then
    printf "File not found: %s\n" "$1"
    exit
fi

if [ -e "$2" ]
then
    printf "File %s already exists, overwrite? [y/N]\n: " "$2"
    read -r yn
    case $yn in
        [Yy]* ) ;;
        * ) exit;;
    esac
fi

inBasename=$(basename "$1")
inExt="${inBasename##*.}"

isVideoStr=$(ffprobe -v warning -show_streams "$1" | grep codec_type=video)
if [ -n "$isVideoStr" ]
then
    isVideo=1
    printf "Detected %s as a video file\n" "$inBasename"
else
    isVideo=0
    printf "Detected %s as an audio file\n" "$inBasename"
fi

printf "Sample noise start time [00:00:00]: "
read -r sampleStart
if [ -z "$sampleStart" ] ; then sampleStart="00:00:00"; fi
printf "Sample noise end time [00:00:00.900]: "
read -r sampleEnd
if [ -z "$sampleEnd" ] ; then sampleEnd="00:00:00.900"; fi
printf "Noise reduction amount [0.21]: "
read -r sensitivity
if [ -z "$sensitivity" ] ; then sensitivity="0.21"; fi


tmpVidFile="/tmp/noiseclean_tmpvid.$inExt"
tmpAudFile="/tmp/noiseclean_tmpaud.wav"
noiseAudFile="/tmp/noiseclean_noiseaud.wav"
noiseProfFile="/tmp/noiseclean_noise.prof"
tmpAudCleanFile="/tmp/noiseclean_tmpaud-clean.wav"

printf "Cleaning noise on %s...\n" "$1"

if [ $isVideo -eq "1" ]; then
    ffmpeg -v warning -y -i "$1" -qscale:v 0 -vcodec copy -an "$tmpVidFile"
    ffmpeg -v warning -y -i "$1" -qscale:a 0 "$tmpAudFile"
else
    cp "$1" "$tmpAudFile"
fi
ffmpeg -v warning -y -i "$1" -vn -ss "$sampleStart" -t "$sampleEnd" "$noiseAudFile"
sox "$noiseAudFile" -n noiseprof "$noiseProfFile"
sox "$tmpAudFile" "$tmpAudCleanFile" noisered "$noiseProfFile" "$sensitivity"
if [ $isVideo -eq "1" ]; then
    ffmpeg -v warning -y -i "$tmpAudCleanFile" -i "$tmpVidFile" -vcodec copy -qscale:v 0 -qscale:a 0 "$2"
else
    cp "$tmpAudCleanFile" "$2"
fi

printf "Done"
