#TRUE :- <DATE TIME> sshd[<RANDOM>]: Accepted publickey for <USERNAME> from <IPADDRESS> port <RANDOM> ssh2
#FAILURE :- <DATE TIME> sshd[<RANDOM>]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=<IPADDRESS>  user=<USERNAME>

#import the modules
import sys
import csv
import logging
import random
from time import sleep
from logging.handlers import SysLogHandler
import syslog
import os

#open file and generate a reader for csv files and close file
fileName  = open(sys.argv[1], "rb")
reader = csv.reader(fileName)

#these statements set up the syslog handler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(sys.argv[2], 514))
logger.addHandler(handler)


#function that ships messages over the network
def logMessages(logData):
    sysLogMessage = ''
    if(logData['Login_Status'] == 'True'):
        sysLogMessage = "sshd[%d]: Accepted publickey for %s from %s port %d ssh2" %(random.randrange(1000, 9999, 345),logData['User'],logData['IP'],random.randrange(1021, 9999, 123))
    else:
        sysLogMessage = "ssshd[%d]: pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=%s user=%s" %(random.randrange(1000, 9999, 345),logData['IP'],logData['User'])

    #log the message in syslogs
    #print sysLogMessage
    logger.info(sysLogMessage)


#the outer for loop generates the headers and inner for loop associates the values to headers
rowNum = 0
for row in reader:
    eachRowData = {}
    # Save header row.
    if rowNum == 0:
        fileData = row

    else:
        colNum = 0
        for col in row:
            eachRowData[fileData[colNum]] = col
            colNum += 1
        if(rowNum % 5 == 0):
            sleep (50.0 / 1000.0)
        logMessages(eachRowData)
    rowNum += 1

fileName.close()




