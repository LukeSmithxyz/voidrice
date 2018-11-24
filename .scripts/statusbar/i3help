#!/bin/sh

case $BLOCK_BUTTON in
    1) groff -mom ~/.readme.mom -Tpdf | zathura - ;;
    3) pgrep -x dunst >/dev/null && notify-send "<b>❓ Help module:</b>
- Left click to open LARBS guide.";;
esac

echo "❓"
