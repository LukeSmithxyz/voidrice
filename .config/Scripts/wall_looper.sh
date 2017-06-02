#!/bin/bash

#Feed this script two arguments, $1 for a folder directory and $2 for a time interval in seconds.

#Will loop thru the files in the directory, using feh to change the background every $2 seconds.

while [ 1==1 ]

do
for file in $1*;
do
sleep $2
feh --bg-scale "$file"
cp "$file" ~/.config/wall.png
done
done
