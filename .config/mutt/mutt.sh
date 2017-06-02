#!/bin/bash
pwds='gpg --decrypt ~/.config/Scripts/DELET'
eval "$pwds"
exec mutt -F ~/.config/mutt/muttrc "$@"
