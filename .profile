#!/bin/sh

# Profile file. Runs on login. Environmental variables are set here.

# Adds `~/.local/bin` to $PATH
export PATH="$PATH:$HOME/.local/bin/"

# Default programs:
export EDITOR="nvim"
export TERMINAL="st"
export BROWSER="tabbed -r 2 surf -e lmao"
export READER="zathura"
export FILE="lf"

# ~/ Clean-up:
export NOTMUCH_CONFIG="$HOME/.config/notmuch-config"
export GTK2_RC_FILES="$HOME/.config/gtk-2.0/gtkrc-2.0"
export LESSHISTFILE="-"
export INPUTRC="$HOME/.config/inputrc"
export ZDOTDIR="$HOME/.config/zsh"
export PASSWORD_STORE_DIR="$HOME/.local/share/password-store"

# Other program settings:
export SUDO_ASKPASS="$HOME/.local/bin/dmenupass"
export LESS=-R
export LESS_TERMCAP_mb="$(printf '%b' '[1;31m')"
export LESS_TERMCAP_md="$(printf '%b' '[1;36m')"
export LESS_TERMCAP_me="$(printf '%b' '[0m')"
export LESS_TERMCAP_so="$(printf '%b' '[01;44;33m')"
export LESS_TERMCAP_se="$(printf '%b' '[0m')"
export LESS_TERMCAP_us="$(printf '%b' '[1;32m')"
export LESS_TERMCAP_ue="$(printf '%b' '[0m')"

[ ! -f ~/.config/shortcutrc ] && shortcuts >/dev/null 2>&1

echo "$0" | grep "bash$" >/dev/null && [ -f ~/.bashrc ] && source "$HOME/.bashrc"

# Start graphical server if i3 not already running.
[ "$(tty)" = "/dev/tty1" ] && ! pgrep -x Xorg >/dev/null && exec startx

# Switch escape and caps if tty:
sudo -n loadkeys ~/.local/share/larbs/ttymaps.kmap 2>/dev/null
