#!/bin/bash

#Feed this script either:
#	"l" for laptop screen only,
#	"v" for vga screen only,
#	or "d" for dual vga/laptop.

d() { if [[ $(xrandr -q | grep VGA1\ con) ]]
	then param $1
	else echo "No VGA input detected."
	fi ;}
dual() { xrandr --output LVDS1 --auto --output VGA1 --auto --right-of LVDS1 ;}
laptop() { xrandr --output LVDS1 --auto --output VGA1 --off ;}
vga() { xrandr --output VGA1 --auto --output LVDS1 --off ;}
#mirror() { xrandr --addmode VGA1 $lapres && xrandr --output LVDS1 --mode $lapres --output VGA1 --mode $lapres ;}

param() {
case $1 in
	d) dual ;;
	v) vga ;;
	l) laptop ;;
	*) echo -e "Invalid parameter. Add one of the following:\n\"d\" for dualscreen laptop and VGA.\n\"l\" for laptop only\n\"v\" for VGA only." ;;
esac ;}
d $1
