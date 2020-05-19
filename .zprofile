#!/bin/zsh

# zsh profile file. Runs on login. Environmental variables are set here.

# If you don't plan on reverting to bash, you can remove the link in ~/.profile
# to clean up.

# Adds `~/.local/bin` to $PATH
export PATH="$PATH:$(du "$HOME/.local/bin/" | cut -f2 | paste -sd ':')"

# Default programs:
export EDITOR="nvim"
export TERMINAL="st"
export BROWSER="brave"
export READER="zathura"

# ~/ Clean-up:
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
## configs
export ALSA_CONFIG_PATH="${XDG_CONFIG_HOME}/alsa/asoundrc"
export ANDROID_SDK_HOME="${XDG_CONFIG_HOME}/android"
export ANSIBLE_CONFIG="${XDG_CONFIG_HOME}/ansible/ansible.cfg"
export GTK2_RC_FILES="${XDG_CONFIG_HOME}/gtk-2.0/gtkrc-2.0"
export INPUTRC="${XDG_CONFIG_HOME}/readline/inputrc"
export NOTMUCH_CONFIG="${XDG_CONFIG_HOME}/notmuch-config"
export WGETRC="${XDG_CONFIG_HOME}/wget/wgetrc"
#export XAUTHORITY="$XDG_RUNTIME_DIR/Xauthority" # This line will break some DMs.
export ZDOTDIR="${XDG_CONFIG_HOME}/zsh"
## program data
export CARGO_HOME="${XDG_DATA_HOME}/cargo"
#export GNUPGHOME="$XDG_DATA_HOME/gnupg"
export GOPATH="${XDG_DATA_HOME}/go"
export KODI_DATA="${XDG_DATA_HOME}/kodi"
export PASSWORD_STORE_DIR="${XDG_DATA_HOME}/password-store"
export TMUX_TMPDIR="${XDG_RUNTIME_DIR}"
export WINEPREFIX="${XDG_DATA_HOME}/wineprefixes/default"

# Misc. program settings:
export DICS="/usr/share/stardict/dic/"
export SUDO_ASKPASS="${HOME}/.local/bin/dmenupass"
export FZF_DEFAULT_OPTS="--layout=reverse --height 40%"
export LESS=-R
export LESSHISTFILE="-"
export LESSOPEN="| /usr/bin/highlight -O ansi %s 2>/dev/null"
export LESS_TERMCAP_mb="$(printf '%b' '[1;31m')"
export LESS_TERMCAP_md="$(printf '%b' '[1;36m')"
export LESS_TERMCAP_me="$(printf '%b' '[0m')"
export LESS_TERMCAP_se="$(printf '%b' '[0m')"
export LESS_TERMCAP_so="$(printf '%b' '[01;44;33m')"
export LESS_TERMCAP_ue="$(printf '%b' '[0m')"
export LESS_TERMCAP_us="$(printf '%b' '[1;32m')"
export AWT_TOOLKIT="MToolkit wmname LG3D" # May have to install wmname.
export MOZ_USE_XINPUT2="1"                # Mozilla smooth scrolling/touchpads.
export QT_QPA_PLATFORMTHEME="gtk2"        # Have QT use gtk2 theme.
export _JAVA_AWT_WM_NONREPARENTING=1      # Fix for Java applications in dwm.

# This is the list for lf icons:
export LF_ICONS="di=📁:\
fi=📃:\
tw=🤝:\
ow=📂:\
ln=⛓:\
or=❌:\
ex=🎯:\
*.1=ℹ:\
*.7z=📦:\
*.R=📊:\
*.Rmd=📊:\
*.avi=🎥:\
*.bib=🎓:\
*.css=🎨:\
*.csv=📓:\
*.djvu=📚:\
*.epub=📚:\
*.flac=🎼:\
*.ged=👪:\
*.gif=🖼:\
*.gpg=🔒:\
*.html=🌎:\
*.ico=🖼:\
*.img=📀:\
*.info=ℹ:\
*.iso=📀:\
*.jpeg=📸:\
*.jpg=📸:\
*.log=📙:\
*.m4a=🎵:\
*.md=📘:\
*.me=✍:\
*.mkv=🎥:\
*.mom=✍:\
*.mp3=🎵:\
*.mp4=🎥:\
*.mpeg=🎥:\
*.ms=✍:\
*.n64=🎮:\
*.nfo=ℹ:\
*.ogg=🎵:\
*.opus=🎵:\
*.part=💔:\
*.pdf=📚:\
*.png=🖼:\
*.r=📊:\
*.rar=📦:\
*.rmd=📊:\
*.svg=🗺:\
*.tar.gz=📦:\
*.tex=📜:\
*.torrent=🔽:\
*.txt=✍:\
*.v64=🎮:\
*.webm=🎥:\
*.xcf=🖌:\
*.xlsx=📓:\
*.xml=📰:\
*.z64=🎮:\
*.zip=📦:\
"

[ ! -f "${XDG_CONFIG_HOME}"/shortcutrc ] && shortcuts >/dev/null 2>&1 &

# Start graphical server on tty1 if not already running.
[ "$(tty)" = "/dev/tty1" ] && ! ps -e | grep -qw Xorg && exec startx "${XDG_CONFIG_HOME}"/X11/xinitrc

# Switch escape and caps if tty and no passwd required:
sudo -n loadkeys "${XDG_DATA_HOME}"/larbs/ttymaps.kmap 2>/dev/null
