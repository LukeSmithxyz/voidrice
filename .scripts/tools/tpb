#!/bin/sh
#
# by Sairon Istyar, 2012
# distributed under the GPLv3 license
# http://www.opensource.org/licenses/gpl-3.0.html
#

### CONFIGURATION ###
# program to use for torrent download
# magnet link to torrent will be appended
# you can add -- at the end to indicate end of options
# (if your program supports it, most do)
program='/usr/bin/transmission-remote -a'
daemon='transmission-daemon'
TPB="https://thepiratebay.org"

# show N first matches by default
limit=50

# colors
numbcolor='\x1b[1;35m'
namecolor='\x1b[1;33m'
sizecolor='\x1b[1;36m'
seedcolor='\x1b[1;31m'
peercolor='\x1b[1;32m'
errocolor='\x1b[1;31m'
mesgcolor='\x1b[1;37m'
nonecolor='\x1b[0m'

# default ordering method
# 1 - name ascending; 2 - name descending;
# 3 - recent first; 4 - oldest first;
# 5 - size descending; 6 - size ascending;
# 7 - seeds descending; 8 - seeds ascending;
# 9 - leechers descending; 10 - leechers ascending;
orderby=7
### END CONFIGURATION ###

thisfile="$0"

printhelp() {
	echo -e "Usage:"
	echo -e "\t$thisfile [options] search query"
	echo
	echo
	echo -e "Available options:"
	echo -e "\t-h\t\tShow help"
	echo -e "\t-n [num]\tShow only first N results (default 15; max 100 [top] or 30 [search])"
	echo -e "\t-C\t\tDo not use colors"
	echo -e "\t-P [prog]\tSet torrent client command (\`-P torrent-client\` OR \`-P \"torrent-client --options\"\`)"
	echo
	echo -e "Current client settings: $program [magnet link]"
}

# change torrent client
chex() {
	sed "s!^program=.*!program=\'$program\'!" -i "$thisfile"
	if [ $? -eq 0 ] ; then
		echo "Client changed successfully."
		exit 0
	else
		echo -e "${errocolor}(EE) ${mesgcolor}==> Something went wrong!${nonecolor}"
		exit 1
	fi
}

# script cmdline option handling
while getopts :hn:CP:: opt ; do
	case "$opt" in
		h) printhelp; exit 0;;
		n) limit="$OPTARG";;
		C) unset numbcolor namecolor sizecolor seedcolor peercolor nonecolor errocolor mesgcolor;;
		P) program="$OPTARG"; chex;;
		*) echo -e "Unknown option(s)."; printhelp; exit 1;;
	esac
done

shift `expr $OPTIND - 1`

# correctly encode query
q=`echo "$*" | tr -d '\n' | od -t x1 -A n | tr ' ' '%'`

# if not searching, show top torrents
if [ -z "$q" ] ; then
	url="top/all"
else
	url='search/'"$q"'/0/'"$orderby"'/0'
fi

# get results
# Here be dragons!
r=`curl -k -A Mozilla -b "lw=s" -m 15 -s "$TPB/$url" \
	| grep -Eo '^<td><a href=\"/torrent/[^>]*>.*|^<td><nobr><a href=\"[^"]*|<td align=\"right\">[^<]*' \
	| sed  's!^<td><a href=\"/torrent/[^>]*>!!; \
		s!</a>$!!; \
		s!^<td><nobr><a href=\"!!; \
		s!^<td [^>]*>!!; \
		s!&nbsp;!\ !g; \
		s/|/!/g' \
	| sed  'N;N;N;N;s!\n!|!g'`

# number of results
n=`echo "$r" | wc -l`

IFS=$'\n'

# print results
echo "$r" \
	| head -n "$limit" \
	| awk -v N=1 \
		-v NU="$numbcolor" \
		-v NA="$namecolor" \
		-v SI="$sizecolor" \
		-v SE="$seedcolor" \
		-v PE="$peercolor" \
		-v NO="$nonecolor" \
		-F '|' \
		'{print NU N ") " NA $1 " " SI $3 " " SE $4 " " PE $5 NO; N++}'

# read ID(s), expand ranges, ignore everything else
read -p ">> Torrents to download (eg. 1 3 5-7): " selection
IFS=$'\n\ '
for num in $selection ; do
	if [ "$num" = "`echo $num | grep -o '[[:digit:]][[:digit:]]*'`" ] ; then
		down="$down $num"
	elif [ "$num" = "`echo $num | grep -o '[[:digit:]][[:digit:]]*-[[:digit:]][[:digit:]]*'`" ] ; then
		seqstart="${num%-*}"
		seqend="${num#*-}"
		if [ $seqstart -le $seqend ] ; then
			down="$down `seq $seqstart $seqend`"
		fi
	fi
done

# normalize download list, sort it and remove dupes
down="$(echo $down | tr '\ ' '\n' | sort -n | uniq)"
IFS=$'\n'

# check whether we're downloading something, else exit
if [ -z "$down" ] ; then
	exit 0
fi

# starts daemon if it was not already running and download all torrents in list
echo -n "Downloading torrent(s): "
if ! [ "$(pidof $daemon)" ]; then
	$daemon
	for torrent in $down ; do
		# check if ID is valid and in range of results, download torrent
		if [ $torrent -ge 1 ] ; then
			if [ $torrent -le $limit ] ; then
				echo -n "$torrent "
				command="$program `echo "$r" | awk -F '|' 'NR=='$torrent'{print $2; exit}'`"
				status=$(eval "$command" 2>&1)
				if [ $? -ne 0 ] ; then
					echo -n '(failed!) '
					report="$report\n(#$torrent) $status"
				fi
			fi
		fi
	done
fi

echo
if [ -n "$report" ] ; then
	echo -n "Exited with errors:"
	echo -e "$report"
fi
unset IFS
