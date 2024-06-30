#!/bin/sh
f="${XDG_DATA_HOME}/urls"
am="@@"
d() { dmenu -i -l "${1}" -p "${2}"; }
no() { notify-send "Bookmarks" "${1}"; }
eno() { no "${1}"; exit; }
pr() { printf "%s\n" "${@}"; }
ch() {
        [ -f "${f}" ] || {
                no "${f} does not exist. Creating it now."
                pr "SearXNG=https://searx.tiekoetter.com/search?q=" > "${f}"
		pr "YouTube=https://www.youtube.com/results?search_query=" >> "${f}"
        }
}
gs() { cut -d= -f1 "${f}" | d "${l}" "Bookmarks"; }
up() { sed -i "s|${1}.*$|${2}|" "${f}"; }
val() { pr "${1}" | grep -qE '^https?://[^\s/$.?#].[^\s]*$'; }
add() {
        u="$(xclip -o)"
        val "${u}" || eno "Clipboard not valid"
        grep -q "=${u}$" "${f}" && eno "URL already saved"
        n="$(pr "" | d "0" "Name")"
        [ "${n}" ] && pr "${n}=${u}" >> "${f}" && no "'${n}' bookmarked"
}
del() {
        n="$(gs)"
        [ "${n}" ] || eno "Failed to delete bookmark"
        sed -i "/^${n}=.*/d" "${f}"
        [ -s "${f}" ] && grep -q "\S" "${f}" || rm "${f}"
        no "'${n}' is deleted."
}
en() {
        on="${1}"
        nn="$(pr "" | d "0" "New Name")"
        [ "${nn}" ] || exit
        u="$(grep "^${on}=" "${f}" | cut -d= -f2)"
        up "^${on}=" "${nn}=${u}"
}
eu() {
        n="${1}"
        nu="$(pr "" | d "0" "New URL")"
        [ "${nu}" ] || exit
        up "${n}=" "${n}=${nu}"
}
eb() {
        n="$(gs)"
        [ "${n}" ] || eno "Failed to edit bookmark"
        fi="$(pr "NAME" "URL" | d "2" "Edit")"
        case "${fi}" in
                "NAME") en "${n}" ;;
                "URL") eu "${n}" ;;
        esac
        no "'${n}' is updated."
}
o() {
        u="$(grep "^${s}=" "${f}" | cut -d= -f2-)"
        [ "${u}" ] || eno "Bookmark not found"
        case "${u}" in
                *"search"* | *"wiki"* | *"packages"*)
                        q="$(pr "" | d "0" "Search")"
                        u="${u}${q}"
                        ;;
        esac
        "${BROWSER}" "${u}" || eno "Failed to open: ${u}"
}
ch
l="$(wc -l < "${f}")"
[ "${l}" -gt "21" ] && l="21"
s="$(gs)"
case "${s}" in
        "${am}")
                a="$(pr "Add" "Delete" "Edit" | d "3" "Action")"
                case "${a}" in "Add") add ;; "Delete") del ;; "Edit") eb ;; esac
                ;;
        "") exit ;;
        *) o ;;
esac
