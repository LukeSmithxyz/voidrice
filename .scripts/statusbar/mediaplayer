#!/usr/bin/env perl
# Copyright (C) 2014 Tony Crisci <tony@dubstepdish.com>
# Copyright (C) 2015 Thiago Perrotta <perrotta dot thiago at poli dot ufrj dot br>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Requires playerctl binary to be in your path (except cmus)
# See: https://github.com/acrisci/playerctl

# Set instance=NAME in the i3blocks configuration to specify a music player
# (playerctl will attempt to connect to org.mpris.MediaPlayer2.[NAME] on your
# DBus session).

use Time::HiRes qw(usleep);
use Env qw(BLOCK_INSTANCE);

use constant DELAY => 50; # Delay in ms to let network-based players (spotify) reflect new data.
use constant SPOTIFY_STR => 'spotify';

my @metadata = ();
my $player_arg = "";

if ($BLOCK_INSTANCE) {
    $player_arg = "--player='$BLOCK_INSTANCE'";
}

sub buttons {
    my $method = shift;

    if($method eq 'mpd') {
        if ($ENV{'BLOCK_BUTTON'} == 1) {
            system("mpc prev");
        } elsif ($ENV{'BLOCK_BUTTON'} == 2) {
            system("mpc toggle");
        } elsif ($ENV{'BLOCK_BUTTON'} == 3) {
            system("mpc next");
        } elsif ($ENV{'BLOCK_BUTTON'} == 4) {
            system("mpc volume +10");
        } elsif ($ENV{'BLOCK_BUTTON'} == 5) {
            system("mpc volume -10");
        }
    } elsif ($method eq 'cmus') {
        if ($ENV{'BLOCK_BUTTON'} == 1) {
            system("cmus-remote --prev");
        } elsif ($ENV{'BLOCK_BUTTON'} == 2) {
            system("cmus-remote --pause");
        } elsif ($ENV{'BLOCK_BUTTON'} == 3) {
            system("cmus-remote --next");
        }
    } elsif ($method eq 'playerctl') {
        if ($ENV{'BLOCK_BUTTON'} == 1) {
            system("playerctl $player_arg previous");
            usleep(DELAY * 1000) if $BLOCK_INSTANCE eq SPOTIFY_STR;
        } elsif ($ENV{'BLOCK_BUTTON'} == 2) {
            system("playerctl $player_arg play-pause");
        } elsif ($ENV{'BLOCK_BUTTON'} == 3) {
            system("playerctl $player_arg next");
            usleep(DELAY * 1000) if $BLOCK_INSTANCE eq SPOTIFY_STR;
        } elsif ($ENV{'BLOCK_BUTTON'} == 4) {
            system("playerctl $player_arg volume 0.01+");
        } elsif ($ENV{'BLOCK_BUTTON'} == 5) {
            system("playerctl $player_arg volume 0.01-");
        }
    } elsif ($method eq 'rhythmbox') {
        if ($ENV{'BLOCK_BUTTON'} == 1) {
            system("rhythmbox-client --previous");
        } elsif ($ENV{'BLOCK_BUTTON'} == 2) {
            system("rhythmbox-client --play-pause");
        } elsif ($ENV{'BLOCK_BUTTON'} == 3) {
            system("rhythmbox-client --next");
        }
    }
}

sub cmus {
    my @cmus = split /^/, qx(cmus-remote -Q);
    if ($? == 0) {
        foreach my $line (@cmus) {
            my @data = split /\s/, $line;
            if (shift @data eq 'tag') {
                my $key = shift @data;
                my $value = join ' ', @data;

                @metadata[0] = $value if $key eq 'artist';
                @metadata[1] = $value if $key eq 'title';
            }
        }

        if (@metadata) {
            buttons('cmus');

            # metadata found so we are done
            print(join ' - ', @metadata);
            exit 0;
        }
    }
}

sub mpd {
    my $data = qx(mpc current);
    if (not $data eq '') {
        buttons("mpd");
        print($data);
        exit 0;
    }
}

sub playerctl {
    buttons('playerctl');

    my $artist = qx(playerctl $player_arg metadata artist);
    chomp $artist;
    # exit status will be nonzero when playerctl cannot find your player
    exit(0) if $? || $artist eq '(null)';

    push(@metadata, $artist) if $artist;

    my $title = qx(playerctl $player_arg metadata title);
    exit(0) if $? || $title eq '(null)';

    push(@metadata, $title) if $title;

    print(join(" - ", @metadata)) if @metadata;
}

sub rhythmbox {
    buttons('rhythmbox');

    my $data = qx(rhythmbox-client --print-playing --no-start);
    print($data);
}

if ($player_arg eq '' or $player_arg =~ /mpd/) {
    mpd;
}
elsif ($player_arg =~ /cmus/) {
    cmus;
}
elsif ($player_arg =~ /rhythmbox/) {
    rhythmbox;
}
else {
    playerctl;
}
print("\n");
