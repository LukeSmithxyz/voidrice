#!/bin/bash

# I don't think this list is everything, please tell me if you find anything missing.

xbps-install xorg-minimal xorg-fonts xf86-input-synaptics xf86-video-intel base-devel xinit xorg-server rxvt-unicode feh ffmpeg arandr mpv wget curl rofi python-pip python-netifaces python-psutil NetworkManager network-manager-applet vim w3m ranger mediainfo poppler highlight tmux calcurse htop newsbeuter moc firefox qutebrowser ImageMagick transmission-gtk transmission atool libcaca compton transset blender gimp texlive MultiMarkdown mupdf evince audacity rsync youtube-dl openssh syncthing noto-fonts-cjk noto-fonts-emoji cups screenFetch neofetch scrot unzip git lmms p7zip font-tamsyn speedometer neomutt font-awesome mypaint pandoc xdotool unclutter-xfixes

tlmgr info collections | grep -o 'collection-[A-Za-z]*' | zargs tlmgr install

git clone https://github.com/ying17zi/vim-live-latex-preview.git
mv vim-live-latex-preview ~/.vim/bundle/ 
