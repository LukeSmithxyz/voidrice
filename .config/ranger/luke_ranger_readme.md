# Luke's ranger setup

## Shortcuts

I've added many folder-specific shortcuts; refer to rc.conf for the specifics, but here's the idea. There are for "verbs:"

+ g -- "go or cd"
+ t -- "new tab"
+ m -- "move file"
+ Y -- "yank or copy file"

These "verbs" take "nouns" or "arguments," like these:

+ d -- "~/Documents"
+ D -- "~/Downloads"
+ cf -- "~/.config"
+ And many others, including those you add!

Press any "verb" followed by any "argument" to perform a folder operation. "gd" will cd to ~/Documents, for example. "mD" will move the selected file(s) to ~/Downloads. "tcf" will create a new tab in ~/.config, etc. etc.

## Many little things!

+ bg -- (for i3 users) makes an image your background (assuming i3 is looking at ~/.config/wall.png for your background)
+ X -- Extract a zip/rar/tar.gz, whatever. Runs a script that picks the right command for the right archive.
+ Z -- zips a folder up into a .tar.gz archive.
+ C -- rotates an image (requires imagemagick)
+ F -- flips an image (requires imagemagick)
+ moc shortcuts
    + MS -- Start server
    + MK -- kill server
    + MN -- Start playing selected song/folder now
    + Ma -- Enqueue selected song/folder
    + Mp -- Pause
    + Mn -- Next track
    + Mb -- Previous track
+ MP -- Convert .md file to .pdf (requires Pandoc)
+ ytv -- Download YouTube video (paste in url) (requires youtube-dl)
+ yta -- Download audio of YouTube video (paste in url) (requires youtube-dl)
