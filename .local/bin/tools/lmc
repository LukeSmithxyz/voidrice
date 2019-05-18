#!/bin/sh
# A general audio interface for LARBS.

[ -z "$2" ] && num="2" || num="$2"

case "$1" in
	u*) pulsemixer --change-volume +"$num" ;;
	d*) pulsemixer --change-volume -"$num" ;;
	m*) pulsemixer --toggle-mute ;;
	truemute) pulsemixer --mute ;;
	play) mpc play ;;
	n*) mpc next ;;
	prev) mpc prev ;;
	t*) mpc toggle ;;
	p*) mpc pause ; pauseallmpv ;;
	f*) mpc seek +"$num" ;;
	b*) mpc seek -"$num" ;;
	r*) mpc seek 0% ;;
	*) cat << EOF
lmc: cli music interface for mpd and pulse for those with divine intellect too
grand to remember the mpc/pamixer commands.

Allowed options:
  up NUM	Increase volume (2 secs default)
  down NUM	Decrease volume (2 secs default)
  mute		Toggle mute
  truemute	Mute
  next		Next track
  prev		Previous track
  toggle	Toggle pause
  truepause	Pause
  foward NUM	Seek foward in song (2 secs default)
  back NUM	Seek back in song (2 secs default)
  restart	Restart current song
  all else	Print this message

All of these commands, except for \`truemute\`, \`prev\` and \`play\` can be truncated,
i.e. \`lmc r\` for \`lmc restart\`.
EOF
esac

pkill -RTMIN+10 i3blocks
