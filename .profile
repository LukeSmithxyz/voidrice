#!/bin/sh

# Profile file. Runs on login.

# variables and default programs:
# Adds `~/.scripts` and all subdirectories to $PATH
export PATH="$(du $HOME/.scripts/ | cut -f2 | tr '\n' ':')$PATH"
export EDITOR="vim"
export TERMINAL="st"
# Link handler is set as the $BROWSER for use with urlscan.
# Set your real browser in $TRUEBROWSER.
export BROWSER="linkhandler"
export TRUEBROWSER="firefox"
export READER="zathura"
export BIB="$HOME/Documents/LaTeX/uni.bib"
export REFER="$HOME/.referbib"
# PIX is here I have LARBS keep icons. Subject to change, hence a variable.
export PIX="$HOME/.scripts/pix"

[ ! -f ~/.shortcuts ] && shortcuts >/dev/null 2>&1

[ -f ~/.bashrc ] && source ~/.bashrc

# Start graphical server if i3 not already running.
if [ "$(tty)" = "/dev/tty1" ]; then
	pgrep -x i3 || exec startx
fi

# Switch escape and caps and use wal colors if tty:
sudo -n loadkeys ~/.scripts/ttymaps.kmap 2>/dev/null
tty | grep tty >/dev/null && wal -Rns
