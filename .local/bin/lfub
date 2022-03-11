#!/bin/sh

# This is a wrapper script for lb that allows it to create image previews with
# ueberzug. This works in concert with the lf configuration file and the
# lf-cleaner script.

set -e

cleanup() {
    exec 3>&-
	rm "$FIFO_UEBERZUG"
}

if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
	lf "$@"
else
	[ ! -d "$HOME/.cache/lf" ] && mkdir -p "$HOME/.cache/lf"
	export FIFO_UEBERZUG="$HOME/.cache/lf/ueberzug-$$"
	mkfifo "$FIFO_UEBERZUG"
	ueberzug layer -s <"$FIFO_UEBERZUG" -p json &
	exec 3>"$FIFO_UEBERZUG"
	trap cleanup HUP INT QUIT TERM PWR EXIT
	lf "$@" 3>&-
fi
