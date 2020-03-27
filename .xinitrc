#!/bin/sh

# xinitrc runs automatically when you run startx.

# There are some small but important commands that need to be run when we start
# the graphical environment. Those commands reside in ~/.xprofile because that
# file runs automatically if someone uses a display manager (login screen)
# and so they are needed there. To prevent doubling up commands, I source them
# here with the line below.

[ -f ~/.xprofile ] && . ~/.xprofile

[ -f ~/.profile ] && . ~/.profile

# if problems occur, log to file for debugging:
#exec i3 -V >> ~/i3log-$(date +'%F-%k-%M-%S') 2>&1
# else:
exec i3
