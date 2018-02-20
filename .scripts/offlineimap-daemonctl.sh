#!/bin/sh
# this script runs offline imap as daemon (configured to check periodically)

LOG=~/.offlineimap/sync.log
PIDFILE=~/.offlineimap/pid

# if not present on PATH, those vars must point to proper locations
THIS_SCRIPT=offlineimap-daemonctl.sh
PYTHON_DAEMON=offlineimap-daemon.py

daemon(){
	$PYTHON_DAEMON 2>&1 |
	# add timestamps to logs
	(while read line; do
		echo `date` "$line" >> $LOG
	done)
}

stop(){
	kill -USR2 `cat $PIDFILE`
}

refresh(){
	kill -USR1 `cat $PIDFILE`
}

case "$1" in
	'--daemon' | '-d' )
		nohup $THIS_SCRIPT < /dev/null > /dev/null 2>&1 &
		;;
	'--kill' | '-k' )
		stop
		;;
	'--refresh' | '-r' )
		refresh
		;;
	* )
		daemon
		;;
esac