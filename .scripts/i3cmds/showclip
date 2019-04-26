#!/bin/sh

# Display contents of selection via dunst if running.
# Separate script for i3.

clip=$(xclip -o -selection clipboard)
prim=$(xclip -o -selection primary)

[ -n "$clip" ] && notify-send "Clipboard:" "$clip"
[ -n "$prim" ] && notify-send "Primary:" "$prim"
