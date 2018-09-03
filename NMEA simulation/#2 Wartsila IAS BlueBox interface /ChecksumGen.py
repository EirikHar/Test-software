#!/bin/env python
"""
Created on Tue May 29 15:03:26 2018

@author: rha
"""

import sys

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

if __name__=='__main__':
    
    line = '$' + sys.argv[1]
         
    print line + make_checksum(line).upper()
    
    
