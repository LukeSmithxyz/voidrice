#!/bin/sh
$HOME/.monicarc   #monitor calibration
[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources
exec i3
