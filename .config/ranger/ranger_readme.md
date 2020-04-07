## Basic Ranger shortcuts

These are the basic key binds in ranger. Note that they are mostly vim-based.

+ h/j/k/l -- Move left/down/up/right (where left moves up in the directory structure, right moves into a folder)
+ Space -- select/highlight file
+ dd -- cut selected files
+ yy -- copy/yank selected files
+ pp -- paste/move cut/copied files
+ / -- search, when (n/N) next/previos result
+ zh or CTRL-h -- show hidden files
+ Renaming files:
	+ cw -- rename file from scratch
	+ A -- rename file adding to the end
	+ aa -- rename file appending before the extension
	+ I -- rename file adding at the beginning

## Shortcuts
For directory shortcuts, here are the "verbs":

+ g -- "go or cd"
+ t -- "new tab"
+ m -- "move file"
+ Y -- "yank or copy file"

These "verbs" take "nouns" or "arguments," like these:

+ d -- "~/documents"
+ D -- "~/downloads"
+ cf -- "~/.config"
+ And many others, including those you add to `~/.directories`.

Press any "verb" followed by any "argument" to perform a folder operation. "gd" will cd to ~/documents, for example. "mD" will move the selected file(s) to ~/downloads. "tcf" will create a new tab in ~/.config, etc. etc.

## Many little additions!

+ Basic additions:
	+ V -- Make a new file and edit it in vim
	+ cW -- rename *all* selected files, editing in your text editor
	+ mkd -- Make a directory/folder
	+ sc -- Makes a link/shortcut (ln -sT)
	+ D -- delete selected file
	+ X -- Extract a zip/rar/tar.gz, whatever. Runs a script that picks the right command for the right archive.
	+ Z -- zips a folder up into a .tar.gz archive.
	+ CTRL-f -- Fuzzy find a file
	+ CTRL-l -- Fuzzy locate a file
+ Document manipulation:
	+ p1s -- print this file on the default printer, one-sided (lpr)
	+ p2s -- print this file on the default printer, double-sided (lpr)
	+ MP -- convert to a .pdf with pandoc (I use this to convert markdown, etc.)
	+ MX -- compile selected document in XeLaTeX
	+ ML -- compile selected document in LaTeX
	+ TC -- clear all non-visible TeX build files in this directory
	+ Txa -- copy article template to new file
	+ Txs -- copy slideshow/beamer template to new file
	+ Txh -- copy handout template to new file
+ Image commands:
	+ bg -- makes an image your background (assuming i3 is looking at ~/.config/assets/wallpaper.png for your background)
	+ bw -- runs Pywal on the selected image, making it your background and generating a color scheme based off of it.
	+ C -- rotates an image (requires imagemagick)
	+ F -- flips an image (requires imagemagick)
	+ TR -- add transparency to image file
+ Downloading:
	+ ytv -- Download online video (paste in url) (requires youtube-dl)
	+ yta -- Download audio of online video (paste in url) (requires youtube-dl)
