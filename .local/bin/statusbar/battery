#!/bin/sh

# Prints all batteries, their percentage remaining and an emoji corresponding
# to charge status (🔌 for plugged up, 🔋 for discharging on battery, etc.).

case $BLOCK_BUTTON in
	3) notify-send "🔋 Battery module" "🔋: discharging
🛑: not charging
♻: stagnant charge
🔌: charging
⚡: charged
❗: battery very low!" ;;
	6) "$TERMINAL" -e "$EDITOR" "$0" ;;
esac

# acpi alternative
# acpi | sed "s/Battery [0-9]: //;s/[Dd]ischarging, /🔋/;s/[Nn]ot charging, /🛑/;s/[Cc]harging, /🔌/;s/[Uu]nknown, /♻️/;s/[Ff]ull, /⚡/;s/ \(remaining\|until charged\)//"; exit

# Loop through all attached batteries.
for battery in /sys/class/power_supply/BAT?
do
	# Get its remaining capacity and charge status.
	capacity=$(cat "$battery"/capacity) || break
	status=$(sed "s/[Dd]ischarging/🔋/;s/[Nn]ot charging/🛑/;s/[Cc]harging/🔌/;s/[Uu]nknown/♻️/;s/[Ff]ull/⚡/" "$battery"/status)

	# If it is discharging and 25% or less, we will add a ❗ as a warning.
	 [ "$capacity" -le 25 ] && [ "$status" = "🔋" ] && warn="❗"

	printf "%s%s%s%% " "$status" "$warn" "$capacity"
	unset warn
done | sed 's/ *$//'
