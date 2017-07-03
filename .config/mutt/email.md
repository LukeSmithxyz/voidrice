# Luke's mutt/OfflineIMAP/msmtp/notmuch setup

## My email setup gives you the following:

+ A clean, fast and vim-like terminal interface to send and read email (mutt)
+ OfflineIMAP, which takes keep a copy of all of your mail offline, allowing you to read and 
+ notmuch as an email indexer, which allows you to easily search email by content within mutt.
+ A looping script which continually uses OfflineIMAP to check mail, and if there is new mail, it will both notify you with a ding and then tell notmuch to quickly index the new mail for searching.

All of these features are well synced together and require just a little setup.

To use my email setup, be sure to have `neomutt`, `offlineimap`, `msmtp` `notmuch` and `notmuch-mutt` installed.

Note that the notification sound will work on i3 by default. You can edit the notification command that runs in `.config/Scripts/check.sh`.

## How to set it up.

To use this setup, you have to add your email settings where required.

There are several steps after which everything should work nicely.

+ **First**, open `.offlineimaprc` and add your email account and server info (details are in that file.
+ To index your mail for quick searching, run `notmuch setup` and give your mail directory (`~/.Mail` by default in my configs)
+ Then you can go ahead and start syncing your email by running `offlineimap -o`. This will download your mail from all the accounts you use to `~/.Mail`.
	+ If you want to use my autosync loop script, make sure to check `.config/Scripts/inboxes` to ensure that your inboxes are there.
+ Next, add your email account info to `.msmtprc`.
+ And the same to `.config/mutt/personalrc` or `.config/mutt/gmailrc` or your own rc file.
	+ (mutt will try to load the `gmailrc` by default. You can change this in `.config/mutt/muttrc`.)

## Updating

As I said before, I have a loop script in `.config/Scripts/mailsyncloop.sh` which will run OfflineIMAPs every few minutes and will play a notification sound and run notmuch if new mail is found.

I suggest running this scipt in a tty or tmux session, so you can check up on it if you really want. That's what I do.

## Enjoy your email!

If you're using my i3 config, you can run mutt with `mutt`. Explore the `muttrc` to see my bindings and add your own.

If you're not using my i3 config, you may want to move `muttrc` to `~/.muttrc`, because I keep my `muttrc` in the `.config` directory to different reasons, but it will look only in `~` by default.
