## Config based upon (Luke Smith <https://lukesmith.xyz>'s dotfiles)

- Very useful scripts are in `~/.local/bin/`
- Settings for:
	- vim/nvim (text editor)
	- zsh (shell)
	- i3wm/i3-gaps (window manager)
	- polybar (status bar)
	- sxhkd (general key binder)
	- ranger (file manager)
	- mpd/ncmpcpp (music)
	- sxiv (image/gif viewer)
	- mpv (video player)
	- calcurse (calendar program)
	- tmux
	- other stuff like xdg default programs, inputrc and more, etc.
- I try to minimize what's directly in `~` so:
	- All configs that can be in `~/.config/` are.
	- Some environmental variables have been set in `~/.zprofile` to move configs into `~/.config/`	
	- Aliases in `~/.config/aliasrc`
	- File bookmarks in `~/.config/files`
	- Directory bookmarks in `~/.config/directories`
	
### Things to add
- show/hide polybar using IPC (polybar-msg)
- Launch pycharm without Jetbrains toolbox (command will look like ``` ./`find .local -name pycharm.sh` ```
