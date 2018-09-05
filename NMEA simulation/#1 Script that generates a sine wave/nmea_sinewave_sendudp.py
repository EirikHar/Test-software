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
    
    
Amp = 9
Fs = 8000
f = 6
sample = 16000
x = np.arange(sample)
y = Amp*(np.sin(2 * np.pi * f * x / Fs))

"""
plt.plot(x,y)
plt.xlabel('sample(n)')
plt.ylabel('Amplitude')
plt.show()
"""

print y
print len(y)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    for value in range(0,len(y)):
        line= "$TEST,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\r\n" %(y[value],y[value]+1,y[value]+2,y[value]+3,y[value]+4,y[value]+5,y[value]+6,y[value]+7,y[value]+8,y[value]+9)
        line= line + make_checksum(line).upper()
        #print(line)        
        time.sleep(0.01)
        print line 

        sock.sendto(bytes(line), ("239.192.239.24",6090))
        #result= subprocess.check_output('echo "%s" > /dev/udp/10.4.1.21/6090' %line)
        #line= "$TEST,%f,%f,%f,%f,%f" %(y[value],y[value]+1,y[value]+2,y[value]+3,y[value]+4,y[value]+5,y[value]+6,y[value]+7,y[value]+8,y[value]+9+random.random())


        
        