#!/bin/sh
[ -f ~/.config/Xresources ] && xrdb -merge ~/.config/Xresources
exec i3
