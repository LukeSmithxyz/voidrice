#!/bin/sh

# xinitrc runs automatically when you run startx.

# There are some small but important commands that need to be run when we start
# the graphical environment. Those commands reside in ~/.xprofile because that
# file runs automatically.

[ -f ~/.xprofile ] && . ~/.xprofile
# [ -f ~/.profile ] && . ~/.profile

# Log to file in $HOME for debugging:
#exec i3 -V >> $HOME/i3log-$(date +'%F-%k-%M-%S') 2>&1
# else:
exec i3
