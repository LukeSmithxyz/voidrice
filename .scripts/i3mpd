#!/bin/bash

# Pass the password in the block instance
if [[ -n $BLOCK_INSTANCE ]]; then
    password=("-h" "$BLOCK_INSTANCE@localhost")
fi

filter() {
	sed 2q | tac | sed -e "s/\&/&amp;/g;/volume:/d;s/\[paused\].*/<span color=\"gray\" font_style=\"italic\">/g;s/\[playing\].*/<span>/g" | tr -d '\n' | sed -e "s/$/<\/span>/g"
	}

case $BLOCK_BUTTON in
    1) mpc $password status | filter && $TERMINAL -e ncmpcpp & disown ;;  # left click, pause/unpause
    3) mpc $password toggle | filter ;;  # right click, pause/unpause
    4) mpc $password prev   | filter ;;  # scroll up, previous
    5) mpc $password next   | filter ;;  # scroll down, next
    *) mpc $password status | filter ;;
esac
