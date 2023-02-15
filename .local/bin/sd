#!/bin/sh

# Open a terminal window in the same directory as the currently active window.

windowPID=$(xprop -id "$(xprop -root | sed -n "/_NET_ACTIVE_WINDOW/ s/^.*# // p")" | sed -n "/PID/ s/^.*= // p")
PIDlist=$(pstree -lpATna "$windowPID" | sed -En 's/.*,([0-9]+).*/\1/p' | tac)
for PID in $PIDlist; do
	cmdline=$(ps -o args= -p "$PID")
	process_group_leader=$(ps -o comm= -p "$(ps -o pgid= -p "$PID" | tr -d ' ')")
	cwd=$(readlink /proc/"$PID"/cwd)
	# zsh and lf won't be ignored even if it shows ~ or /
	case "$cmdline" in
		'lf -server') continue ;;
		"${SHELL##*/}"|'lf'|'lf '*) break ;;
	esac
	# git (and its sub-processes) will show the root of a repository instead of the actual cwd, so they're ignored
	[ "$process_group_leader" = 'git' ] || [ ! -d "$cwd" ] && continue
	# This is to ignore programs that show ~ or / instead of the actual working directory
	[ "$cwd" != "$HOME" ] && [ "$cwd" != '/' ] && break
done
[ "$PWD" != "$cwd" ] && [ -d "$cwd" ] && { cd "$cwd" || exit 1; }
"$TERMINAL"
