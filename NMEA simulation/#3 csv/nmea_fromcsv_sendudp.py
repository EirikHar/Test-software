# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 10:27:31 2018

@author: eirikh
"""

import subprocess
import matplotlib.pyplot as plt
import numpy as np
import time
import random
import socket

def make_checksum( msg ):
    """
    Make a NMEA 0183 checksum on a string. Skips leading ! or $ and stops
    at *
    It ignores anything before the first $ or ! in the string
    """

    # Find the start of the NMEA sentence
    startchars = "!$"
    for c in startchars:
        i = msg.find(c)
        if i >= 0: break
    else:
        return (False, None, None)

    # Calculate the checksum on the message
    sum1 = 0
    for c in msg[i+1:]:
        if c == '*':
	    break;
        sum1 = sum1 ^ ord(c)
    sum1 = sum1 & 0xFF
    
    return "*" + hex(sum1).replace("0x", '')

def sendNmea(nmea_name, ai_row):
    nmea_output1 = "$%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(nmea_name,ai_row[1],ai_row[2],ai_row[3],ai_row[4],ai_row[5],ai_row[6],ai_row[7],ai_row[8],ai_row[9],ai_row[10])
    nmea_output1 = nmea_output1 + make_checksum(nmea_output1).upper()+"\r\n"
    #print(line)        
    print nmea_output1.strip()
    sock.sendto(bytes(nmea_output1), ("10.4.1.21",6090))

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)    

while True:
    files = []
    files.append(open("LOGAI.txt"))
    files.append(open("LOGINT.txt"))
    files.append(open("LOGSAI.txt"))
    files.append(open("LOGTNK.txt"))

    hasMoreData = True

    while hasMoreData:
        i = 1
        for csvfile in files:
            rowline = csvfile.readline().strip()
            if len(rowline) < 1:
                print('Reached end of file! Restarting')
                hasMoreData = False
                break
            row = rowline.split(";")
            sendNmea("UPC"+str(i), row)
            i += 1
 #       print('sleeping')
        time.sleep(1)
#        print('sleep done')
   
            
            
            
            
            
            



        
        