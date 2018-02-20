#!/bin/bash

base=$(basename $1)
ext="${base##*.}"
base="${base%.*}"

ffmpeg -i $1 -vf "setpts=$2*PTS" -an $base'_sped.'$ext
