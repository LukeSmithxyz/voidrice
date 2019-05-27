# Luke's GNU/Linux Dotfiles

These are my dotfiles! The name of the repo, "voidrice", came from the fact they were originally on my Void Linux machine, but these files are distro-independent. In fact, I now push changes from my X200 running Parabola or my X220 running Arch.

## Programs whose configs can be found here

+ i3 (i3-gaps)
+ ~~Xresourses/Xdefaults settings~~ Now moved to [my terminal (st) build](https://github.com/lukesmithxyz/st) which uses them
+ vim
+ bash
+ vifm
+ ~~mutt/msmtp/offlineimap~~ Now moved to [LukeSmithxyz/mutt-wizard](https://github.com/LukeSmithxyz/mutt-wizard)
+ calcurse
+ ncmpcpp and mpd (my main music player)
+ mpv
+ And many little scripts I use filed in the `~/.local/bin/` directory

## More documentation

There's a full .pdf write-up of the repository [here: https://larbs.xyz/larbs_readme.pdf](https://larbs.xyz/larbs_readme.pdf).

Or, if you actually installed my dotfiles, you can just press `Super+F1` to
show the same document offline.

In the system, you can also press `Super+Shift+e` to watch tutorial videos on
different programs used. See [my YouTube channel](https://youtube.com/c/LukeSmithxyz) for more.

The command `getkeys` will also show basic key binds for different programs.

## Dynamic Configuration Files

Store your favorite or high-traffic directories in `~/.config/bmdirs` or your most
important config files in `~/.config/bmfiles` with keyboard shortcuts. When you add
things to theses files my vimrc will automatically run `shortcuts` which will
dynamically generate shortcuts for these in bash, ranger and optionally
qutebrowser and fish.

## Like my rice?

Feel free to add other suggestions and I may implement them.

I have a job, but every penny I get from followers or subscribers is more incentive to perfect what I'm doing.
You can donate to me at [https://paypal.me/LukeMSmith](https://paypal.me/LukeMSmith).
Donations are earmarked for whatever the donator wants, usually to go to funds for buying new equipment for the [YouTube channel](https://youtube.com/c/LukeSmithxyz).

# "Dependencies" and programs used

The programs I use here are always changing, but luckily you can just look at the installation list for [LARBS](http://larbs.xyz) here:

+ [List of programs installed by LARBS, including optional packages](https://github.com/LukeSmithxyz/LARBS/blob/master/archi3/progs.csv)

`A` marks programs in the AUR, `G` marks git repositories.
