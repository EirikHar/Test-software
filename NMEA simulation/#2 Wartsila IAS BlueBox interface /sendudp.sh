#!/bin/bash

FS=$'\n'      
while true
do
    for j in `cat NMEA`
	do
        NmeaString=$(python ChecksumGen.py $j)
        echo "Send string: " $NmeaString 
        echo $NmeaString > /dev/udp/10.4.1.21/6090
    	sleep 0.1
	done
done 
