#!/bin/sh

# opout: "open output": A general handler for opening a file's intended output,
# usually the pdf of a compiled document.  I find this useful especially
# running from vim.

basename="${1%.*}"

case "${*}" in
	*.tex|*.sil|*.m[dse]|*.[rR]md|*.mom|*.[0-9]) target="$(getcomproot "$1" || echo "$1")" ; setsid -f xdg-open "${target%.*}".pdf >/dev/null 2>&1 ;;
	*.html) setsid -f "$BROWSER" "$basename".html >/dev/null 2>&1 ;;
	*.sent) setsid -f sent "$1" >/dev/null 2>&1 ;;
esac
