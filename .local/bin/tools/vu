#!/usr/bin/env sh
export FIFO_UEBERZUG="/tmp/vifm-ueberzug-${PPID}"

cleanup() {
    rm "$FIFO_UEBERZUG" 2>/dev/null
    pkill -P $$ 2>/dev/null
}

rm "$FIFO_UEBERZUG" 2>/dev/null
mkfifo "$FIFO_UEBERZUG"
trap cleanup EXIT
tail --follow "$FIFO_UEBERZUG" | ueberzug layer --silent --parser bash &

vifm
cleanup
