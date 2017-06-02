#!/bin/bash

sex=$(ffprobe -i $1 -show_entries format=duration -v quiet -of csv="p=0")
rate=$(qalc -t 1000000000 / $sex)
#rate=$(( 1000000000 / $sex ))

base=$(basename $1)
ext="${base##*.}"
base="${base%.*}"

ffmpeg -i $1 -b $rate $base'_min.'$ext
echo "sex is $sex"
echo "rate is $rate"
