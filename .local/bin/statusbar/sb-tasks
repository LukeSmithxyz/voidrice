#!/bin/sh

# Originally by Andr3as07 <https://github.com/Andr3as07>
# Some changes by Luke
# Rebuild by Tenyun

# This block displays the number running background tasks.  Requires tsp.

num=$(tsp -l | awk -v numr=0 -v numq=0 '{if (/running/)numr++; if (/queued/)numq++} END{print numr+numq"("numq")"}')

# Handle mouse clicks
case $BLOCK_BUTTON in
	1) setsid -f "$TERMINAL" -e tsp -l ;;
	3) notify-send "Tasks module" "🤖: number of running/queued background tasks
- Left click opens tsp" ;; # Right click
	2) $EDITOR "$0" ;; # Middle click
esac

[ "$num" != "0(0)" ] &&
	echo "🤖$num"
