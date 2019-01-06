#!/bin/sh

# Display contents of selection via dunst if running.
# Separate script for i3.

! pgrep -x dunst >/dev/null && echo "dunst not running." && exit

clip=$(xclip -o -selection clipboard)

prim=$(xclip -o -selection primary)

[ "$clip" != "" ] && notify-send "<b>Clipboard:</b>
$clip"
[ "$prim" != "" ] && notify-send "<b>Primary:</b>
$prim"
