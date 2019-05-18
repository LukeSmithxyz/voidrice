# Directory of Scripts

I keep all my user-created scripts here in `~/.local/bin/`.  Scripts are sorted
into sub-directories for easy management, and all are seamlessly added to
`$PATH` with the command below in `~/.profile`:

```
export PATH="$(du $HOME/.local/bin/ | cut -f2 | tr '\n' ':')$PATH"
```

## `statusbar/`

For modules used in i3blocks.

- `battery` -- i3blocks module. Shows available power remaining with icon indicating battery status. Colors indicate different levels of charge.
- `clock` -- Shows time and date. If clicked, brings up calender or coming calcuse events.
- `cpu` -- Shows CPU temperature. If clicked, shows most processor-intensive processes.
- `help` -- Module which appears as a question mark. Brings up readme if clicked.
- `internet` -- Shows whether machine is connected to wifi and ethernet. If clicked, brings up `nmtui`.
- `mailbox` -- i3blocks module for use with mutt-wizard. Shows unread mail and if `mailsync.sh` is running.
- `mem` -- Shows memory usage. If clicked, shows most memory-intensive processes.
- `music` -- i3blocks module. Shows current song; if paused, name will be grayed and italic.
- `mpdupdate` -- A daemon running by default that will update the i3mpd block on mpd change.
- `news` -- Shows unread newsboat articles. Brings up newsboat or refreshes RSS feeds.
- `pacpackages` -- i3blocks module. Detects new installable upgrades. Only works if you use cronjobs to automatically sync repositories.
- `popupgrade` -- Called by clicking on the update icon if there are new packages. Spawns a `yay` upgrade of the main Arch repos and AUR packages, updates the i3blocks module once complete.
- `torrent` -- i3blocks module. Shows torrents idle (⌛️), downloading (⬇️) or finished (🌱).
- `volume` -- i3blocks module. Shows volume percentage or mute notification.
- `weather` -- i3blocks module. Gets weather forcast from wttr.in and returns today's precipitation chance (☔), daily low (❄️) and daily high (☀️).

## `cron/`

For scripts meant to be cronjobs. None are active by default on LARBS.

- `checkup` -- If connected to internet, syncs package repositories and downloads (but does not install) any potential updates. Gives `notify-send` notifications of when it is active since other `pacman` install commands cannot be run simultaneously. You may need to grant your user the ability to run `pacman -Syyuw --noconfirm` without a password (done in `/etc/sudoers`).
- `cronbat` -- Gives a dunst notification if the battery is less than 25%.
- `crontog` -- Not actually a cronjob, but just turns off/on all user cronjobs.
- `getforecast` -- Updates the weather forecast. This is automatically run by `weather` if there hasn't been a new forecast today.
- `newsup` -- Updates newsboat RSS feeds if connected to internet. Will also display a newspaper update icon on i3blocks if it has not be user disabled.

## `tools/`

Scripts intended to be run either manually by the user or linked to a shortcut
in vim or another program.

- `compiler` -- Compiles a markdown, R markdown or LaTeX document with the approriate command.  Will also run `make && sudo make install` if in a `config.h` file.  Otherwise it will create a sent presentation.  This can be thought of a general output handler.  I have it bound to `<leader>c` in vim.
- `dmenuhandler` -- Give this script a url and it will offer dmenu options for opening it. Used by `newsboat` and some other programs as a link handler.
- `extract` -- Will detect file type of archive and run appropriate extraction command.
- `getbib` -- Use crossref.org to automatically detect bibtex entry of a .pdf. Attempts to search for the .pdf's DOI. Returns nothing if none detected.
- `getkeys` -- Get the LARBS documentation on what bindings exist for main programs.
- `linkhandler` -- The automatic link handler used by `newsboat` and other programs. Urls of video sites or of video files are opened in `mpv`, images are downloaded/opened in `feh`, music files are downloaded with `wget` and all other urls are opened in the default browser.
- `lmc` -- A music controller that simplifies music/audio management and improves the interface with i3blocks. Check inside to see what it does. This is what i3 audio/music commands run by default. If you use a difference music system or ALSA, you can change this script rather than changing all the shortcuts in different places.
- `note` -- Give this script some text/a message as an argument. It will print it to the terminal, and if `dunst` is running, display a notification.
- `opout` -- "Open output", opens the corresponding `.pdf` file if run on a `.md`, `.tex` or `.rmd` file, or if given an `.html` file, will open it in the browser.  Bound to `<leader>p` in my vim config to reveal typical output.
- `pauseallmpv` -- Pauses all mpv instances by sending the `,` key to each. Used by several scripts, but can be used alone as well. It will not pause an audio only mpv instance. If you know how to add a hack to do this, feel free to PR it or email me an addition.
- `remaps` -- Remaps capslock to escape when pressed and super/mod when held. Maps the menu key to super as well. Runs the US international keyboard setup. If you want another keyboard setup, edit this fine.
- `shortcuts` -- For updating bash and ranger shortcuts. Reads `~/.config/bmdirs` and `~/.config/bmfiles` for pairs of keypresses and directories and files, then autoproduces bash aliases and ranger shortcuts for them which output to `~/.config/shortcutrc` and `~/.config/ranger/shortcuts.conf` respectively. These are read automatically by my bash and ranger configs. You don't have to run this script manually though, as it's run by vim whenever you edit one of the `~/.bm*` files.
- `speedvid` -- Speed up a given video file (`$1`) by a given ammount (`$2`).
- `tpb` -- Search Pirate Bay for the certain search terms given as arguments.
- `texclear` -- Remove all `.tex` related build files. This is run by my vim when I stop editing any `.tex` file.
- `transadd` -- The mimeapp default script for handling torrent magnet links. Starts `transmission-daemon` if not running and adds the link.

## `i3cmds`

These are scripts linked to bindings in i3. They typically perform
user-interface actions or involve dmenu.

- `bottomleft` and `bottomright` -- Makes the currently selected window float in one of the bottom corners of the screen. `bottomleft` is bound to `mod+B` by default.
- `camtoggle` -- Starts/kills /dev/video0 webcam. Placed in bottom right by default.
- `ddspawn` -- This is the script called to create, show and hide the dropdown tmux terminal mapped to `mod+u`, but also the dropdown calculator mapped to `mod+a`. Give the script an argument that is a script the window will run. If a window does not already exist, `ddspawn` creates it, if it does, `ddspawn` will toggle its visibility. The the script itself for usage.
- `displayselect` -- Select which displays to use. Bound to `mod+F3`.
- `dmenumount` -- Gives a dmenu prompt for mounting USB drives or Android devices. Bound to `mod+F9`. Will do nothing if none are available.
- `dmenurecord` -- Gives a list of recording commands: `audio`, `video` and `screencast` (both) in dmenu for selection. Bound to `mod+PrintScreen` by default. Should be killed by `killrecording`.
- `dmenuumount` -- Unmount a mounted non-essential partition. Bound to `mod+F10`. Will do nothing if none are mounted. It will not try to unmount essential system partitions.
- `dmenuunicode` -- Shows a searchable dmenu prompt of emoji characters. The selected emoji is copied to the system clipboard, while its character code is copied to primary selection (middle mouse button).
- `dropdowncalc` -- The dropdown calculator script called by `ddspawn` and bound to `mod+a` by default. Will run an R calculator if installed, otherwise python.
- `ducksearch` -- Show a dmenu prompt and search for the inputed text in DuckDuckGo. Can take bangtags as expected, i.e. typing in `!aw Arch Linux` will search the Arch Wiki for "Arch Linux" or `!yt Luke Smith` will search YouTube for "Luke Smith", etc.
- `i3resize` -- A script that allows intuitive resizing of windows. Mapped to `mod+Y/U/I/O`.
- `killrecording` -- End a recording started by `dmenurecord` the proper way without file trucation or lingering background processes, mapped to `mod+Delete` by default.
- `lockscreen` -- The screen locker. Gives a confirm prompt and if user says yes, all audio will be paused and the screen will be distorted and locked and screen will soon time out. User must insert password to unlock. Mapped to `mod+x` by default.
- `newspod` -- A silly line that has a script all to itself due to i3's idiosyncracies. Starts `newsboat`, if `newsboat` cannot open because of another instance being open, opens `podboat`.
- `prompt` -- Gives a Yes/No prompt to a question given as an argument. Used by numerous bindings like `mod+shift+x`, `mod+shift+backspace` and `mod+shift+escape`.
- `samedir` -- Opens a terminal window in the same directory as the window currently selection. Bound to `mod+shift+enter`.
- `td-toggle` -- Gives a dmenu prompt to start `transmission-daemon` if not running, or the kill it if it is. Obviously you need `transmission-cli` installed for this to work.  Mapped to `mod+F7` by default.
- `tmuxdd` -- The startup script for the dropdown terminal (toggleable with `mod+u`). Either attaches to an existing tmux session or begins a new one.
- `toggletouchpad` -- As the name suggests, turns off TouchPad if on, and turns it on if off. Requires `xf86-input-synaptics`. If your laptop has a special button for this, it will be mapped by default.
- `tutorialvids` -- A dmenu prompt that gives some options of tutorial videos to watch. Bound to `mod+shift+e`.
