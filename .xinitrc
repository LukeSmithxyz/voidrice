#!/bin/sh

# fixes problems with mysql-workbench
# and maybe other problems
# eval $(/usr/bin/gnome-keyring-daemon --start --components=gpg,pkcs11,secrets,ssh)
# export $(gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg)
# dbus-update-activation-environment --systemd DISPLAY
# END

# fixes problems with mysql-workbench
# and maybe other problems
dbus-update-activation-environment --systemd DISPLAY
eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh)
export SSH_AUTH_SOCK
# END

[ -f ~/.Xmodmap ] && xmodmap ~/.Xmodmap
[ -f ~/.Xresources ] && xrdb -merge ~/.Xresources

setxkbmap -model extd -layout gb,gr -option grp:alt_shift_toggle

xset r rate 200 50

# from arch wiki for thinkpad x230
xrandr --dpi 125.37

# cat ~/.config/i3/config ~/.config/i3/config.custom > ~/.config/i3/config.combined

exec i3
