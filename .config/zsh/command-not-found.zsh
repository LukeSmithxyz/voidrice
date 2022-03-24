# This script was borrowed and then customized from the ArchWiki:
# https://wiki.archlinux.org/title/Zsh#pacman_-F_"command_not_found"_handler

function command_not_found_handler {
	local purple='\e[1;35m' bright='\e[0;1m' green='\e[1;32m' reset='\e[0m'
	printf 'zsh: command not found: %s\n' "$1"
	local entries=(
		${(f)"$(/usr/bin/pacman -F --machinereadable -- "/usr/bin/$1")"}
	)
	if (( ${#entries[@]} )); then
		printf "${bright}%s${reset} may be found in the following packages:\n" "$1"
		local pkg
		for entry in "${entries[@]}"; do
			local fields=(${(0)entry})
			if [[ "$pkg" != "${fields[2]}" ]]; then
				printf "  ${purple}%s/${bright}%s ${green}%s${reset}\n" "${fields[1]}" "${fields[2]}" "${fields[3]}"
			fi
		done
	fi
	return 127
}
