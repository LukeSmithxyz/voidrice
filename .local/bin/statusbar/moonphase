#!/bin/sh

mnphs=$(pom $1 | grep -o 'New\|Waxing Crescent\|First Quarter\|Waxing Gibbous\|Full\|Waning Gibbous\|Last Quarter\|Waning Crescent' | grep -m1 '.')
prcnt=$(pom $1 | grep -o '[[:digit:]]*%')
case "$mnphs" in
	"New") icon="🌑" prcnt="0%" ;;
	"Waxing Crescent") icon="🌒" ;;
	"First Quarter") icon="🌓" prcnt="50%" ;;
	"Waxing Gibbous") icon="🌔" ;;
	"Full") icon="🌕" prcnt="100%" ;;
	"Waning Gibbous") icon="🌖" ;;
	"Last Quarter") icon="🌗" prcnt="50%" ;;
	"Waning Crescent") icon="🌘" ;;
	*) echo errorrrr ;;
esac

printf "%s %s\\n" "$icon" "$prcnt"
