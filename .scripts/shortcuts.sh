#!/bin/bash

# Config locations
folders="$HOME/.scripts/folders"
configs="$HOME/.scripts/configs"

# Output locations
bash_shortcuts="$HOME/.bash_shortcuts"
ranger_shortcuts="$HOME/.config/ranger/shortcuts.conf"
qute_shortcuts="$HOME/.config/qutebrowser/shortcuts.py"

# Ensuring that output locations are properly sourced
cat ~/.bashrc | grep "source ~/.bash_shortcuts" >/dev/null &&
	echo Bashrc already ready. ||
	(echo "source ~/.bash_shortcuts" >> ~/.bashrc &&
	echo Bashrc now prepared for shortcuts.)

cat ~/.config/ranger/rc.conf | grep "source ~/.config/ranger/shortcuts.conf" >/dev/null &&
	echo Rc.conf already ready. ||
	(echo "source ~/.config/ranger/shortcuts.conf" >> ~/.config/ranger/rc.conf &&
	echo rc.conf now prepared for shortcuts.)

cat ~/.config/qutebrowser/config.py | grep shortcuts.py >/dev/null &&
	echo "Qutebrowser's config.py already ready." ||
	(echo "config.source('shortcuts.py')" >> ~/.config/qutebrowser/config.py &&
	echo "qutebrowser's config.py now prepared for shortcuts.")

#Delete old shortcuts
echo "# vim: filetype=sh" > $bash_shortcuts
echo "# ranger shortcuts" > $ranger_shortcuts
echo "# qutebrowser shortcuts" > $qute_shortcuts

writeDirs() { echo "alias $1='cd $2 && ls -a'" >> $bash_shortcuts
	echo "map g$1 cd $2" >> $ranger_shortcuts
	echo "map t$1 tab_new $2" >> $ranger_shortcuts
	echo "map m$1 shell mv %s $2" >> $ranger_shortcuts
	echo "map Y$1 shell cp -r %s $2" >> $ranger_shortcuts
	echo "config.bind(';$1', 'set downloads.location.directory $2 ;; hint links download')" >> $qute_shortcuts ;}

writeConfs() {
	echo "alias $1='vim $2'" >> $bash_shortcuts
	echo "map $1 shell vim $2" >> $ranger_shortcuts ;}

IFS=$'\n'
set -f
for line in $(cat "$folders"); do
	line=$(echo $line | sed 's/#.*//')
	key=$(echo $line | awk '{print $1}')
	dir=$(echo $line | awk '{print $2}')
	[ "$dir" == "" ] || writeDirs $key $dir
done && echo "Directory shortcuts done."

set -f
for line in $(cat "$configs");
do
	line=$(echo $line | sed 's/#.*//')
	short=$(echo $line | awk '{print $1}')
	conf=$(echo $line | awk '{print $2}')
	[ "$conf" == "" ] || writeConfs $short $conf
done && echo "Config file shortcuts done."

echo "All done!"
