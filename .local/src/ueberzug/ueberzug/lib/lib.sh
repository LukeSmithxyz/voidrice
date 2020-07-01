#!/usr/bin/env bash
function String::trim {
    while read line; do
        printf %s\\n "$line"
    done
}


function Error::raise {
    local -a stack=()
    local stack_size=${#FUNCNAME[@]}

    for ((i = 1; i < $stack_size; i++)); do
        local caller="${FUNCNAME[$i]}"
        local line_number="${BASH_LINENO[$(( i - 1 ))]}"
        local file="${BASH_SOURCE[$i]}"
        [ -z "$caller" ] && caller=main

        stack+=(
            # note: lines ending with a backslash are counted as a single line
            $'\t'"File ${file}, line ${line_number}, in ${caller}"
            $'\t\t'"`String::trim < "${file}" | head --lines "${line_number}" | tail --lines 1`"
        )
   done

   printf '%s\n' "${@}" "${stack[@]}" 1>&2
   exit 1
}


function Map::escape_items {
    while (( "${#@}" > 0 )); do
        local key="${1%%=[^=]*}"
        local value="${1#[^=]*=}"
        printf "%s=%q " "$key" "$value"
        shift
    done
}


function ImageLayer {
    ueberzug layer -p bash "$@"
}

function ImageLayer::__build_command {
    local -a required_keys=( $1 ); shift
    local -A data="( `Map::escape_items "$@"` )"

    for key in "${required_keys[@]}"; do
        # see: https://stackoverflow.com/a/13221491
        if ! [ ${data["$key"]+exists} ]; then
            Error::raise "Key '$key' missing!"
        fi
    done

    declare -p data
}

function ImageLayer::build_command {
    local action="$1"; shift
    local required_keys="$1"; shift
    ImageLayer::__build_command "action $required_keys" [action]="$action" "$@"
}

function ImageLayer::add {
    ImageLayer::build_command add "identifier x y path" "$@"
}

function ImageLayer::remove {
    ImageLayer::build_command remove "identifier" "$@"
}
