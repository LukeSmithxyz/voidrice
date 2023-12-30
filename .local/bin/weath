#!/bin/sh
#
# Get the weather on the terminal. You can pass an alternative location as a parameter,
# and/or use the 'cp' option to copy the forecast as plaintext to the clipboard.

report="${XDG_CACHE_HOME:-$HOME/.cache}/weatherreport"

if [ "$1" = 'cp' ]; then
        # shellcheck disable=SC2015
        [ -z "$2" ] && sed 's/\x1b\[[^m]*m//g' "$report" | xclip -selection clipboard &&
                notify-send "Weather forecast for '${LOCATION:-$(head -n 1 "$report" | cut -d' ' -f3-)}' copied to clipboard." ||
                        { data="$(curl -sfm 5 "${WTTRURL:-wttr.in}/$2?T")" &&
                        notify-send "Weather forecast for '$2' copied to clipboard." &&
                        echo "$data" | xclip -selection clipboard ||
                        notify-send 'Failed to get weather forecast!' 'Check your internet connection and the supplied location.'; }
else
        [ -n "$2" ] &&
                notify-send "Invalid option '$1'! The only valid option is 'cp'." &&
                exit 1

        # shellcheck disable=SC2015
        [ -z "$1" ] && less -S "$report" ||
                data="$(curl -sfm 5 "${WTTRURL:-wttr.in}/$1")" && echo "$data" | less -S ||
                        notify-send 'Failed to get weather forecast!' 'Check your internet connection and the supplied location.'
fi
