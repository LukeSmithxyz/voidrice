#!/usr/bin/env sh

# xinitrc runs automatically when you run startx.

guesswm() {
	# Here, LARBS decides whether to boot dwm or i3. It will boot what is manually
	# set in ~/.local/share/larbs/wm, otherwise it will test to see if dwm is
	# installed, in which case it will load dwm. It will assume i3 otherwise.

	LARBSWM="$(cat ~/.local/share/larbs/wm 2>/dev/null)" ||
		{ LARBSWM="$(type dwm >/dev/null 2>&1)" && LARBSWM="dwm" ;} ||
		{ LARBSWM="$(type i3 >/dev/null 2>&1)" && LARBSWM="i3" ;}

	# To be clear, you can run:
	#	echo dwm > ~/.local/share/larbs/wm
	# to set dwm as your default LARBS WM (or echo i3 for i3).

	# Here we start the window manager, whichever it's supposed to be.
	# Note that we set the different status bar commands here too.

	case "$LARBSWM" in
		dwm)
			export FILE="lf"
			export STATUSBAR="dwmblocks"
			startlarbs() { # The loop is just to enable dwm's "restart" feature (mod+F2).
				while :; do
					ssh-agent dwm || break
				done ;}
			;;
		i3)
			export FILE="ranger"
			export STATUSBAR="i3blocks"
			startlarbs() { exec i3 ;}
			;;
		*) echo "No valid LARBS window manager detected." ;;
	esac ;}

guesswm

# There are some small but important commands that need to be run when we start
# the graphical environment. I keep those commands in ~/.xprofile because that
# file is run automatically if someone uses a display manager (login screen)
# and so they are needed there. To prevent doubling up commands, I source them
# here with the line below.

[ -f ~/.xprofile ] && . ~/.xprofile

startlarbs
