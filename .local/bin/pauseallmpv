#!/bin/sh

# You might notice all mpv commands are aliased to have this input-ipc-server
# thing. That's just for this particular command, which allows us to pause
# every single one of them with one command! This is bound to super + shift + p
# (with other things) by default and is used in some other places.

for i in $(ls /tmp/mpvSockets/*); do
	echo '{ "command": ["set_property", "pause", true] }' | socat - "$i";
done
