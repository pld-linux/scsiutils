#!/bin/sh
# Skript to rescan SCSI bus, using the 
# scsi add-single-device mechanism
# (w) 98/03/19 Kurt Garloff <kurt@garloff.de> (c) GNU GPL

# Return hosts. /proc/scsi/HOSTADAPTER/? must exist
findhosts ()
{
	hosts=
	for name in /proc/scsi/*/?; do
		name=${name#/proc/scsi/}
		if test ! $name = scsi ; then
			hosts="$hosts ${name#*/}"
			echo "Host adapter ${name#*/} (${name%/*}) found."
		fi
	done
}

# Test if SCSI device $host $channen $id $lun exists
# Outputs description from /proc/scsi/scsi, returns new
testexist ()
{
	grepstr="scsi$host Channel: 0$channel Id: 0*$id Lun: 0$lun"
	new=`cat /proc/scsi/scsi|grep -e"$grepstr"`
	if test ! -z "$new" ; then
		cat /proc/scsi/scsi|grep -e"$grepstr"
		cat /proc/scsi/scsi|grep -A2 -e"$grepstr"|tail -2|pr -o4 -l1
	fi
}

# Perform search (scan $host)
dosearch ()
{
    for channel in $channelsearch; do
	for id in $idsearch; do
	    for lun in $lunsearch; do
		new=
		devnr="$host $channel $id $lun"
		echo "Scanning for device $devnr ..."
		printf "OLD: "
		testexist
		if test ! -z "$remove" -a ! -z "$new" ; then
		    echo "scsi remove-single-device $devnr" >/proc/scsi/scsi
		    echo "scsi add-single-device $devnr" >/proc/scsi/scsi
		    printf "\r\x1b[A\x1b[A\x1b[AOLD: "
		    testexist
		    if test -z "$new"; then
			printf "\rDEL: \r\n\n\n\n";
			let rmvd+=1;
		    fi
		fi
		if test -z "$new" ; then
		    printf "\rNEW: "
		    echo "scsi add-single-device $devnr" >/proc/scsi/scsi
		    testexist
		    if test -z "$new"; then
			printf "\r\x1b[A"
		    else
			let found+=1;
		    fi
		fi
	    done
	done
    done
}
	  
  
# main

if [ ! -e /proc/scsi ]; then
	echo "You don't have SCSI, go away!"
	exit 1
fi

if [ "$1" = "--help" -o "$1" = "-h" ]; then 
	echo "Usage: rescan-scsi-bus.sh [-l] [-w] [-c] [host [host ...]]"
	echo " -l	activates scanning for LUNs 0..7	[default: 0]"
	echo " -w	enables scanning for device IDs 0..15	[def.: 0..7]"
	echo " -r	enables removing of devices		[default: disabled]"
	echo " -c	enables scanning of channels 0 1	[default: 0]"
	echo " If hosts are given, only these are scanned	[default: all]"
	exit 0
fi

# defaults
lunsearch="0"
idsearch="0 1 2 3 4 5 6 7"
channelsearch="0"
remove=""

# Scan options
opt="$1"
while [ ! -z "$opt" -a -z "${opt##-*}" ]; do
	opt=${opt#-}
	case "$opt" in
	    l) lunsearch="0 1 2 3 4 5 6 7" ;;
	    w) idsearch="0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15" ;;
	    c) channelsearch="0 1" ;;
	    r) remove=1 ;;
	    *) echo "Unknown option -$opt !" ;;
	esac
	shift
	opt="$1"
done    

# Hosts given ?
if [ -z $1 ]; then
	findhosts
else
	hosts=$*
fi

declare -i found=0
declare -i rmvd=0
for host in $hosts; do
	dosearch
done
echo "$found new device(s) found."
echo "$rmvd device(s) removed."
 echo "Options:"
    echo " -l activates scanning for LUNs 0-7    [default: 0]"
    echo " -w scan for target device IDs 0 .. 15 [default: 0-7]"
    echo " -c enables scanning of channels 0 1   [default: 0]"
    echo " -r enables removing of devices        [default: disabled]"
    echo "--remove:        same as -r"
    echo "--nooptscan:     don't stop looking for LUNs is 0 is not found"
    echo "--color:         use coloured prefixes OLD/NEW/DEL"
    echo "--hosts=LIST:    Scan only host(s) in LIST"
    echo "--channels=LIST: Scan only channel(s) in LIST"
    echo "--ids=LIST:      Scan only target ID(s) in LIST"
    echo "--luns=LIST:     Scan only lun(s) in LIST"  
    echo " Host numbers may thus be specified either directly on cmd line (deprecated) or"
    echo " or with the --hosts=LIST parameter (recommended)."
    echo "LIST: A[-B][,C[-D]]... is a comma separated list of single values and ranges"
    echo " (No spaces allowed.)"
    exit 0
fi

expandlist ()
{
    list=$1
    result=""
    first=${list%%,*}
    rest=${list#*,}
    while test ! -z "$first"; do 
	beg=${first%%-*};
	if test "$beg" = "$first"; then
	    result="$result $beg";
    	else
    	    end=${first#*-}
	    result="$result `seq $beg $end`"
	fi
	test "$rest" = "$first" && rest=""
	first=${rest%%,*}
	rest=${rest#*,}
    done
    echo $result
}

# defaults
unsetcolor
lunsearch="0"
idsearch=`seq 0 7`
channelsearch="0"
remove=""
optscan=1
findhosts;

# Scan options
opt="$1"
while test ! -z "$opt" -a -z "${opt##-*}"; do
  opt=${opt#-}
  case "$opt" in
    l) lunsearch=`seq 0 7` ;;
    w) idsearch=`seq 0 15` ;;
    c) channelsearch="0 1" ;;
    r) remove=1 ;;
    -remove)      remove=1 ;;
    -hosts=*)     arg=${opt#-hosts=};   hosts=`expandlist $arg` ;;
    -channels=*)  arg=${opt#-channels=};channelsearch=`expandlist $arg` ;; 
    -ids=*)   arg=${opt#-ids=};         idsearch=`expandlist $arg` ;; 
    -luns=*)  arg=${opt#-luns=};        lunsearch=`expandlist $arg` ;; 
    -color) setcolor ;;
    -nooptscan) optscan=0 ;;
    *) echo "Unknown option -$opt !" ;;
  esac
  shift
  opt="$1"
done    

# Hosts given ?
if test @$1 != @; then 
  hosts=$*; 
fi

echo "Scanning hosts $hosts channels $channelsearch for "
echo " SCSI target IDs " $idsearch ", LUNs " $lunsearch
test -z "$remove" || echo " and remove devices that have disappeared"
declare -i found=0
declare -i rmvd=0
for host in $hosts; do 
  dosearch; 
done
echo "$found new device(s) found.               "
echo "$rmvd device(s) removed.                 "

