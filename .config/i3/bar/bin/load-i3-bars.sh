#!/usr/bin/env bash

if [ ! -f ~/.i3/config.template ]; then
	cp ~/.i3/config ~/.i3/config.template
else
	cp ~/.i3/config.template ~/.i3/config
fi

screens=$(xrandr -q|grep ' connected'| grep -P '\d+x\d+' |cut -d' ' -f1)

echo "screens: $screens"

while read -r line; do
	screen=$(echo $line | cut -d' ' -f1)
	others=$(echo $screens|tr ' ' '\n'|grep -v $screen|tr '\n' '-'|sed 's/.$//')

	if [ -f ~/.i3/config.$screen-$others ]; then
		cat ~/.i3/config.$screen-$others >> ~/.i3/config
	else
		if [ -f ~/.i3/config.$screen ]; then
			cat ~/.i3/config.$screen >> ~/.i3/config
		fi
	fi
done <<< "$screens"

i3-msg restart
