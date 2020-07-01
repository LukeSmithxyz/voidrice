#!/usr/bin/env bash
# This is just an example how ueberzug can be used.
# Copyright (C) 2019  Nico Baeurer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
source "`ueberzug library`"

readonly USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
declare -g target_host

function unpack {
    local tmp="${@/[^(]*\(}"
    echo -n "${tmp%)}"
}

function Api::discover {
    local -A params="( `unpack "$@"` )"
    local -a hosts=( "${params[host]}" )
    local -A added

    declare -p params
    declare -p hosts

    for ((i=0; i < ${#hosts[@]} && ${#hosts[@]} < ${params[max]}; i++)); do
        #echo
        #echo [i=$i, ${#hosts[@]}/${params[max]}] Querying ${hosts[$i]}
        local -a results=(`curl --user-agent "${USER_AGENT}" "${hosts[$i]}/api/v1/timelines/public?limit=40" 2>/dev/null | \
            jq -r '.[].url' 2>/dev/null | \
            grep -oP 'https?://[^.]+\.[^/]+'`)

        for host in "${results[@]}"; do
            if ! [ ${added["$host"]+exists} ]; then
                added["$host"]=True
                hosts+=( "$host" )
            fi
        done
    done

    declare -p hosts
}

function Api::get_local_timeline {
    local host="$1"
    local -a urls="( `{ curl --fail --user-agent "${USER_AGENT}" "${host}/api/v1/timelines/public?local=true&only_media=true&limit=40" 2>/dev/null || 
        curl --user-agent "${USER_AGENT}" "${host}/api/v1/timelines/public?local=true&limit=40" 2>/dev/null ; } | \
        jq -r '.[].media_attachments[].preview_url' 2>/dev/null | \
        sort -u` )"
    declare -p urls
}

function Array::max_length {
    local -a items=( "$@" )
    local max=0

    for i in "${items[@]}"; do
        if (( ${#i} > max )); then
            max=${#i}
        fi
    done

    echo $max
}

declare -g screen_counter=0

function Screen::new {
    let screen_counter+=1
    tput smcup 1>&2
}

function Screen::pop {
    tput rmcup 1>&2
    let screen_counter-=1
}

function Screen::move_cursor {
    tput cup "$1" "$2" 1>&2
}

function Screen::hide_cursor {
    tput civis 1>&2
}

function Screen::show_cursor {
    tput cnorm 1>&2
}

function Screen::width {
    tput cols
}

function Screen::height {
    tput lines
}

function Screen::cleanup {
    while ((0 < screen_counter)); do
        Screen::pop
    done
    Screen::show_cursor
}

function Screen::popup {
    local -a message=( "$@" )
    local line_length="`Array::max_length "${message[@]}"`"
    local line_count="${#message[@]}"
    local offset_x="$(( `Screen::width` / 2 - line_length / 2 ))"
    local offset_y="$(( `Screen::height` / 2 - ( line_count + 1 ) / 2 ))"

    Screen::new

    for ((i=0; i < ${#message[@]}; i++)); do
        Screen::move_cursor $(( offset_y + i )) $offset_x
        echo "${message[$i]}" 1>&2
        Screen::move_cursor $(( offset_y + 1 + i )) $offset_x
    done
}

function Screen::dropdown {
    local offset_y="$(( `Screen::height` / 2 - 1 ))"
    local title="$1"
    shift

    Screen::new
    Screen::hide_cursor
    Screen::move_cursor $offset_y 1
    smenu -m "$title" -M -W' '$'\n' -t 1 -l  <<<"${@}"
}

function Screen::select_host {
    local -A params="( `unpack "$@"` )"
    Screen::popup 'Searching hosts' \
                  "Searching up to ${params[max]} mastodon instances," \
                  "using ${params[host]} as entry point."
    Screen::hide_cursor
    local -A hosts="( $(unpack "`Api::discover "$@"`") )"
    Screen::pop

    echo -n "$(Screen::dropdown "Select host:" "${hosts[@]}")"
    Screen::pop
}

function Screen::display_media {
    local -a urls=( "$@" )

    ImageLayer 0< <(
        function cleanup {
            if [[ "$tmpfolder" == "/tmp/"* ]]; then
                rm "${tmpfolder}/"*
                rmdir "${tmpfolder}"
            fi
        }
        trap 'cleanup' EXIT

        padding=3
        width=40
        height=14
        page_width=`Screen::width`
        page_height=`Screen::height`
        full_width=$(( width + 2 * padding ))
        full_height=$(( height + 2 * padding ))
        cols=$(( page_width / full_width ))
        rows=$(( page_height / full_height ))
        page_media_count=$(( rows * cols ))
        offset_x=$(( (page_width - cols * full_width) / 2 ))
        offset_y=$(( (page_height - rows * full_height) / 2 ))
        iterations=$(( ${#urls[@]} / ( cols * rows ) ))
        tmpfolder=`mktemp --directory`

        for ((i=0; i < iterations; i++)); do
            for ((r=0; r < rows; r++)); do
                for ((c=0; c < cols; c++)); do
                    index=$(( i * page_media_count + r * rows + c ))
                    url="${urls[$index]}"
                    name="`basename "${url}"`"
                    path="${tmpfolder}/$name"
                    curl --user-agent "${USER_AGENT}" "${url}" 2>/dev/null > "${path}"
                    ImageLayer::add [identifier]="${r},${c}" \
                                    [x]="$((offset_x + c * full_width))" [y]="$((offset_y + r * full_height))" \
                                    [max_width]="$width" [max_height]="$height" \
                                    [path]="$path"
                    Screen::move_cursor "$((offset_y + (r + 1) * full_height - padding + 1))" "$((offset_x + c * full_width))"
                    echo -n "$name" 1>&2
                done
            done

            read
            
            for ((r=0; r < rows; r++)); do
                for ((c=0; c < cols; c++)); do
                    ImageLayer::remove [identifier]="${r},${c}"
                done
            done

            clear 1>&2
        done
    )
}

function Screen::display_timeline {
    local -A params="( `unpack "$@"` )"
    local -A urls="( $(unpack "`Api::get_local_timeline "${params[host]}"`") )"
    Screen::new
    Screen::hide_cursor

    if (( ${#urls[@]} == 0 )); then
        Screen::pop
        Screen::popup "There was no image in the current feed."
        read
        Screen::pop
        return
    fi

    Screen::display_media "${urls[@]}"
    Screen::pop
}

trap 'Screen::cleanup' EXIT
target_host="$(Screen::select_host [max]=30 [host]="https://mastodon.social")"

if [ -n "$target_host" ]; then
    Screen::display_timeline [host]="$target_host"
fi
