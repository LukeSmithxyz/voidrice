# Luke's mutt readme, Part 2: Offline IMAPS

Here was my goal:

+ Have an extensible terminal based email client that can store all of my emails offline for access when I don't have internet.

This is important, not just for general convenience, but because I don't have internet for most of the day.

## OfflineIMAPS

OfflineIMAPS keeps a local repo of your IMAP emails on your own machine. I've done the setup in this rice for you, you just have to fill in your account info.

## Setup

Look up your server info for your email provider. The details will be on their website.

First go to `~/.offlineimaprc`. I have a template for a Gmail account there already. You can simply add your username and password in the required locations. You can add or replace the gmail account with any other kind of email account as well, just instead of `type = Gmail`, use `type = IMAP` in the remote repository. Note that each email account will have a general settings category, marked [Account NAME] and two sub repositories, one being the online repo and the other being a directory on your own machine, marked [Repository NAME-remote] and [Repository NAME-local]. To add new accounts mimic the syntax I have.

Then either run `offlineimap -o` and if your information was entered correctly, OfflineIMAP will begin to download *all* of your email (which may take a while).

Next add your account and (SMTP) server info to `~/.msmtp`. This will allow you to send emails.

## How to keep synced

Each time you run `offlineimap`, mail will be synced between the internet and your own machine. I don't have a systematized way to run this, but `~/.config/Scripts/mailsyncloop.sh` is aliased to `mailsync` and will updateOfflineIMAP every couple of minutes or so. There are smarter ways to do this, and if you develop one, feel free to tell me!

[luke@lukesmith.xyz](mailto:luke@lukesmith.xyz)
