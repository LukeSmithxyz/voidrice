#!/bin/bash

for d in /dev/sd*
do

while IFS=$'\t' read -r col1 col2
do
	if [[ $(blkid -o value -s UUID $d) == ${col2} ]]
	then
	sudo mkdir /mnt/${col1}
	sudo mount $d /mnt/${col1}
	fi
done < /home/kulade/.config/Scripts/drives

done

