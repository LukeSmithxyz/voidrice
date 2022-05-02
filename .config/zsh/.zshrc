# Luke's config for the Zoomer Shell

export ZSH="$HOME/.config/zsh/oh-my-zsh"
# History in cache directory:
HISTSIZE=10000000
SAVEHIST=10000000
HISTFILE="${XDG_CACHE_HOME:-$HOME/.cache}/zsh/history"

ZSH_THEME="agnoster"
DEFAULT_USER=$(whoami)

# Load aliases and shortcuts if existent.
[ -f "${XDG_CONFIG_HOME:-$HOME/.config}/shell/shortcutrc" ] && source "${XDG_CONFIG_HOME:-$HOME/.config}/shell/shortcutrc"
[ -f "${XDG_CONFIG_HOME:-$HOME/.config}/shell/aliasrc" ] && source "${XDG_CONFIG_HOME:-$HOME/.config}/shell/aliasrc"
[ -f "${XDG_CONFIG_HOME:-$HOME/.config}/shell/zshnameddirrc" ] && source "${XDG_CONFIG_HOME:-$HOME/.config}/shell/zshnameddirrc"

# Basic auto/tab complete:
zstyle ':completion:*' menu select
zmodload zsh/complist

# Use vim keys in tab complete menu:
bindkey -M menuselect 'h' vi-backward-char
bindkey -M menuselect 'k' vi-up-line-or-history
bindkey -M menuselect 'l' vi-forward-char
bindkey -M menuselect 'j' vi-down-line-or-history
bindkey -v '^?' backward-delete-char

plugins=(git colored-man-pages)

source $ZSH/oh-my-zsh.sh

_comp_options+=(globdots)

motdmaker && cat ~/.cache/motd
