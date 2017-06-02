# Luke's mutt readme

mutt is a terminal email program.

## Using my configs

Move the muttrc file to  ~/.muttrc to activate it by default.

Make an rc file for your own email address. If you have a Gmail account, for example, modify the "gmailrc" file to your address. Make sure muttrc is sourcing the file you want.

You should also have Neomutt installed for full compatibility.

## Macros and shortcuts

I've made some changes to the bindings to make mutt a little more vim-like. See them in muttrc for yourself.

I've also employed gotbletu's shortcuts for changing accounts and moving from Inbox to Sent to Drafts etc.

Note that the commands for movement to different boxes are in the individual email configs. This is because the folder structure of each account may differ. When mutt loads another email account, it also loades the new shortcuts. You may need to make changes for your email account.

## Colors and themes

My muttrc has my particular formats for email headers and date.

You have a lot of freedom in how you can configure how mutt works. Here, I have a file "muttcol" which is originally someone else's theme (can't remember where I got it), but I've also made color changes in the muttrc.

My config is made for Neomutt, which allows email headers to have different colors for different information. If you're not running Neomutt, you'll get errors when using my configs. To remove these errors delete the following lines from the muttrc:

color index_author red default '.*'
color index_number blue default
color index_subject cyan default '.s'
color index_size green default

## Aliases

You can use aliases to avoid having to type out email addresses over and over. For example, if you have the following:

alias luke luke@lukesmith.xyz

whenever you type in "luke" as a recipient, it will automatically direct that you my email. You can also have aliases for groups of people, separated by a comma.

alias best_friends billy@gmail.com, sally@gmail.com, amanda@gmail.com, chad@gmail.com

so whenever you type in "best_friends," mutt will direct the mail to all four of these email addresses.

## Passwords

If you don't want mutt to ask for your password when logging on, set imap_pass to your password.

imap_pass = muh_password


Same is true of smtp_pass if you want to send emails without a password.

smtp = muh_password

There are securer ways of storing your pass word, which you can research youself. I'm still figuring out an elegant solution that works for me.

## To come...

I'm still figuring out offlineIMAPs and some other little things to interface with mutt. I'll put up a new video when I'm totally successful.
