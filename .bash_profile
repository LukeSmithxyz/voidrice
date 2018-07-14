#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

export PATH="$PATH:$HOME/.scripts"
export EDITOR="vim"
export TERMINAL="st"
export BROWSER="firefox"

# Uncomment lines below to autostart i3 when logged in:
#if [[ "$(tty)" = "/dev/tty1" ]]; then
	#pgrep i3 || exec startx
#fi
