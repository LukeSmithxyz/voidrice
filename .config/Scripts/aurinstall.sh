#!/bin/bash
wget https://aur.archlinux.org/cgit/aur.git/snapshot/$1.tar.gz
tar -xvzf $1.tar.gz
cd $1 && makepkg --no-confirm -si
cd .. && rm -rf $1 $1.tar.gz
