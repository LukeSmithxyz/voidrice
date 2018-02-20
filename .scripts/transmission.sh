#!/bin/bash
if [ -f $(pgrep transmission) ];
	then
	urxvt -e transmission-remote-cli
	else
	transmission-daemon && urxvt -e transmission-remote-cli
fi
