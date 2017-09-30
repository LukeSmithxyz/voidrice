#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

#if [ -z "$DISPLAY" ] && [ "$(fgconsole)" -eq 1 ]; then
	#startx
#fi

#[ -z "$DISPLAY" -a "$(fgconsole)" -eq 1 ] && exec startx

if [[ -f /usr/bin/waterfox ]]; then
	export BROWSER="waterfox"
elif [[ -f /usr/bin/palemoon ]]; then
	export BROWSER="palemoon"
elif [[ -f /usr/bin/iceweasel ]]; then
	export BROWSER="iceweasel"
else
	export BROWSER="firefox"
fi
