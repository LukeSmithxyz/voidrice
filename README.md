# The Voidrice (Luke Smith <https://lukesmith.xyz>'s dotfiles)

These are the dotfiles deployed by [LARBS](https://larbs.xyz) and as seen on [my YouTube channel](https://youtube.com/c/lukesmithxyz).

- Very useful scripts are in `~/.local/bin/`
- Settings for:
	- vim/nvim (text editor)
	- sxhkd (general key binder)
	- lf (file browser)
	- mpd/ncmpcpp (music)
	- sxiv (image/gif viewer)
	- mpv (video player)
- I try to minimize what's directly in `~` so:
	- All configs that can be in `~/.config/` are.
	- Some environmental variables have been set in `~/.profile` to move configs into `~/.config/`
- Bookmarks in text files used by various scripts
	- File bookmarks in `~/.config/files`
	- Directory bookmarks in `~/.config/directories`

## I'm looking for i3, ranger, etc. Where are they?

There are two branches in this repository, `master`, which I use myself and regularly update (using dwm as a window manager), and `archi3` which is an older an more-or-less constant branch that contains older dotfiles, including those for programs I no longer use (like ranger) and which runs i3 as a window manager.
If problems arise with my i3 configuration here, you'll have to bring them up to me since I no longer use it.
I'd estimate that more of my subscribers use i3 rather than dwm, so I keep it here for them.

My setup is pretty modular nowadays.
I use several suckless program that are meant to be configured and compiled by the user and I also have separate repos for some other things.
Check out their links:

- [dwm](https://github.com/lukesmithxyz/dwm) (the window manager)
- [st](https://github.com/lukesmithxyz/st) (the terminal emulator)
- [mutt-wizard (`mw`)](https://github.com/lukesmithxyz/mutt-wizard) - (a terminal-based email system that can store your mail offline without effort)

## Install these dotfiles

Use [LARBS](https://larbs.xyz) to autoinstall everything:

```
curl -LO larbs.xyz/larbs.sh
```

or clone the repo files directly to your home directory and install [the prerequisite programs](https://github.com/LukeSmithxyz/LARBS/blob/master/progs.csv) or [those required for the i3 setup](https://github.com/LukeSmithxyz/LARBS/blob/master/legacy.csv).
