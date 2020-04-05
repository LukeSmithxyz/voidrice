#!/bin/sh

printf "Beginning upgrade.\\n"

yay -Syu
pkill -RTMIN+8 "${STATUSBAR:?}"

printf "\\nUpgrade complete.\\nPress <Enter> to exit window.\\n\\n"
read -r
