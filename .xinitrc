#!/bin/sh
[ -f ~/.config/Xresources ] && xrdb -merge ~/.config/Xresources
xset r rate 200 50
exec i3
