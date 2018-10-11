# Directory of Scripts

## `audio`

The audio recording script run by `dmenurecord` (bound to `mod+Print`).

## `bottomleft`

Makes the currently selected window float in the bottom left of screen. Bound
to `mod+B`.

## `camtoggle`

Starts/kills /dev/video0 webcam. Placed in bottom right by default.

## `compiler`

Compiles a markdown, R markdown or LaTeX document with the approriate command.
Will also run `make && sudo make install` if in a `config.h` file.  Otherwise
it will create a sent presentation.  This can be thought of a general output
handler.  I have it bound to `<leader>c` in vim.

## `crontog`

Turns off/on all user cronjobs.

## `displayselect`

Select which displays to use. Bound to `mod+F3`.

## `dmenuarchwiki`

Bind this script to a key and it will give you a prompt to search for a term in
the Arch Wiki. Used to be binded to `mod+F11`, but has been replaced by
`ducksearch` there.

## `dmenuhandler`

Give this script a url and it will offer dmenu options for opening it. Used by
`newsboat` and some other programs as a link handler.

## `dmenumount`

Detect available partitions with `lsblk` and offer to mount them. Bound to
`mod+F9`. Will do nothing if none are available.

## `dmenurecord`

Gives a list of recording commands: `audio`, `video` and `screencast` (both) in
dmenu for selection.

## `dmenuumount`

Unmount a mounted non-essential partition. Bound to `mod+F10`. Will do nothing
if none are mounted.

## `dropdowncalc`

The command initially run in the `math` window (toggeable with `mod+a`). Runs
`r` if available, else `python`.

## `ducksearch`

Show a dmenu prompt and search for the inputed text in DuckDuckGo. Can take
bangtags as expected, i.e. typing in `!aw Arch Linux` will search the Arch Wiki
for "Arch Linux" or `!yt Luke Smith` will search YouTube for "Luke Smith", etc.

## `extract`

Will detect file type of archive and run appropriate extraction command.

## `getbib`

Use crossref.org to automatically detect bibtex entry of a .pdf. Attempts to
search for the .pdf's DOI. Returns nothing if none detected.

## `getkeys`

Get the LARBS documentation on what bindings exist for main programs.

## `i3battery`

i3blocks module. Shows available power remaining with icon indicating battery
status. Colors indicate different levels of charge.

## `i3mail`

i3blocks module for use with mutt-wizard. Shows unread mail and if
`mailsync.sh` is running.

## `i3mpd`

i3blocks module. Shows current song; if paused, name will be grayed and italic.

## `i3mpdupdate`

A daemon running by default that will update the i3mpd block on mpd change.

## `i3pacman`

i3blocks module. Detects new installable upgrades. Only works if you use
cronjobs to automatically sync repositories.

## `i3resize`

A script that allows intuitive resizing of windows. Mapped to `mod+Y/U/I/O`.

## `i3torrent`

i3blocks module. Shows torrents idle (⌛️), downloading (⬇️) or
finished (🌱).

## `i3volume`

i3blocks module. Shows volume percentage or mute notification.

## `i3weather`

i3blocks module. Gets weather forcast from wttr.in and returns today's
precipitation chance (☔), daily low (❄️) and daily high (☀️).

## `i3wifi`

A modified version of the i3blocks wifi module. Clicked, it brings up wifi-menu
and also appears when there is no wifi connection.

## `kb-lights.py`

A Python 3 script which will increase or decrease keyboard lights when given
either a `+` or `-` argument.

## `killrecording`

End a recording started by `dmenurecord` the proper way.

## `linkhandler`

The automatic link handler used by `newsboat` and other programs. Urls of video
sites or of video files are opened in `mpv`, images are downloaded/opened in
`feh`, music files are downloaded with `wget` and all other urls are opened in
the default browser.

## `lmc`

A music controller that simplifies music/audio management and improves the
interface with i3blocks. Check inside to see what it does. This is what i3
audio/music commands run by default. If you use a difference music system or
ALSA, you can change this script rather than changing all the shortcuts in
different places.

## `lockscreen`

The screen locker. Gives a confirm prompt and if user says yes, all audio will
be paused and the screen will be distorted and locked and screen will soon time
out. User must insert password to unlock.

## `musstuff`

Some old notes and commands on deleted music shortcuts.

## `note`

Give this script some text/a message as an argument. It will print it to the
terminal, and if `dunst` is running, display a notification.

## `opout`

"Open output", opens the corresponding `.pdf` file if run on a `.md`, `.tex` or
`.rmd` file, or if given an `.html` file, will open it in the browser.  Bound
to `<leader>p` in my vim config to reveal typical output.

## `pauseallmpv`

Pauses all mpv instances by sending the `,` key to each. Used by several
scripts, but can be used alone as well.

## `polybar_launch`

For `polybar` users. Launches `polybar` on every screen. Should be run in the
i3 config.

## `popweather`

The script called by clicking on the i3 weather module. Brings up the forecast
from `http://wttr.in` and waits for input to prevent immediate closing of
spawned window.

## `prompt`

Gives a Yes/No prompt to a question given as an argument. Used by numerous
bindings like `mod+shift+x`, `mod+shift+backspace` and `mod+shift+escape`.

## `remaps`

Remaps capslock to escape when pressed and super/mod when held. Maps the menu
key to super as well. Runs the US international keyboard setup. If you want
another keyboard setup, edit this fine.

## `samedir`

Opens a terminal window in the same directory as the window currently
selection. Bound to `mod+shift+enter`.

## `screencast`

A script for `dmenurecord`. Records default audio and the screen.

## `shortcuts.sh`

For updating bash and ranger shortcuts. Reads `~/.scripts/folders` and
`~/.scripts/configs` for pairs of keypresses and directories and configfiles,
then autoproduces bash aliases and ranger shortcuts for them. See the
`README.md` at
[https://github.com/LukeSmithxyz/shortcu-sync](https://github.com/LukeSmithxyz/shortcu-sync)
for the specifics.

## `texclear`

Remove all `.tex` related build files. This is run by my vim when I stop
editing any `.tex` file.

## `tmuxinit`

The startup script for the dropdown terminal (toggleable with `mod+u`). Either
attaches to an existing tmux session or begins a new one.

## `toggletouchpad`

As the name suggests, turns off TouchPad if on, and turns it on if off.
Requires `xf86-input-synaptics`.

## `tpb`

Search Pirate Bay for the certain search terms given as arguments.

## `tutorialvids`

A dmenu prompt that gives some options of tutorial videos to watch. Bound to
`mod+shift+e`.

## `video`

A script for `dmenurecord`. Records the screen with no audio.
