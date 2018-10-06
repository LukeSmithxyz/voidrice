#!/bin/sh

printf "Beginning upgrade.\\n"

yay -Syu
pacman -Qu | wc -l > ~/.pacupgrnum
pkill -RTMIN+8 i3blocks

printf "\\nUpgrade complete.\\nPress <Enter> to exit window.\\n\\n"
read -r
