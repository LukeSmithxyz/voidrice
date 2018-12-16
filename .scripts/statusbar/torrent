#!/bin/sh

transmission-remote -l | grep % |
	sed " # This first sed command is to ensure a desirable order with sort
	s/.*Stopped.*/A/g;
	s/.*Seeding.*/Z/g;
	s/.*100%.*/N/g;
	s/.*Idle.*/B/g;
	s/.*%.*/M/g" |
		sort -h | uniq -c | sed " # Now we replace the standin letters with icons.
				s/A/🛑/g;
				s/B/⌛️/g;
				s/M/🔽/g;
				s/N/✅/g;
				s/Z/🌱/g" | awk '{print $2, $1}' | tr '\n' ' ' | sed -e "s/ $//g"

case $BLOCK_BUTTON in
    1) $TERMINAL -e transmission-remote-cli ;;
    3) pgrep -x dunst >/dev/null && notify-send "<b>Torrent module:</b>
🛑: paused
⏳: waiting
🔽: downloading
✅: done
🌱: done and seeding" ;;
esac

