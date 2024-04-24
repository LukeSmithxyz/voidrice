#!/bin/sh

# A dmenu wrapper script for system functions.
export WM="dwm"
case "$(readlink -f /sbin/init)" in
	*systemd*) ctl='systemctl' ;;
	*) ctl='loginctl' ;;
esac

wmpid(){ # This function is needed if there are multiple instances of the window manager.
	tree="$(pstree -ps $$)"
	tree="${tree#*$WM(}"
	echo "${tree%%)*}"
}

case "$(printf "🔒 lock\n🚪 leave $WM\n♻️ renew $WM\n🐻 hibernate\n🔃 reboot\n🖥️shutdown\n💤 sleep\n📺 display off" | dmenu -i -p 'Action: ')" in
	'🔒 lock') slock ;;
	"🚪 leave $WM") kill -TERM "$(wmpid)" ;;
	"♻️ renew $WM") kill -HUP "$(wmpid)" ;;
	'🐻 hibernate') slock $ctl hibernate -i ;;
	'💤 sleep') slock $ctl suspend -i ;;
	'🔃 reboot') $ctl reboot -i ;;
	'🖥️shutdown') $ctl poweroff -i ;;
	'📺 display off') xset dpms force off ;;
	*) exit 1 ;;
esac
