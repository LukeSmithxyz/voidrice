#!/bin/bash
NUM=$(cat /sys/class/power_supply/BAT0/capacity)
STATE=$(cat /sys/class/power_supply/BAT0/status)

colorget() {
if [[ $NUM -ge 80 ]]; then
	color="#00FF00"
elif [[ $NUM -ge 60 ]]; then
	color="#FFFFFF"
elif [[ $NUM -ge 40 ]]; then
	color="#FFF600"
elif [[ $NUM -ge 20 ]]; then
	color="#FFAE00"
else
	color="#FF0000"
fi ;}

if [[ $STATE == "Charging" ]]; then
	 color="#ffffff"
else
	colorget
fi

echo "<span color='$color'>$(echo $STATE | sed -e "s/,//g;s/Discharging/🔋/;s/Charging/🔌/;s/Unknown/❓/;s/Full/⚡/;s/ 0*/ /g;s/ :/ /g") $(echo $NUM | sed -e 's/$/%/')</span>"
