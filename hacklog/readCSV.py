#import the modules
from time import sleep
from logging.handlers import SysLogHandler
import syslog
import sys
import csv
import logging
import random
import os


#function that ships messages over the network
def logMessages(logData):
    sysLogMessage = ''
    if(logData['Login_Status'] == 'True'):
        sysLogMessage = "sshd[%d]: Accepted publickey for %s from %s port %d ssh2" %(random.randrange(1000, 9999, 345),logData['User'],logData['IP'],random.randrange(1021, 9999, 123))
    else:
        sysLogMessage = "ssshd[%d]: pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=%s user=%s" %(random.randrange(1000, 9999, 345),logData['IP'],logData['User'])

    #log the message in syslogs
    logger.info(sysLogMessage)

#this function reads each log from the csv
#forms a dictionary with appropriate values
#calls a function logMessages that forms the log messages based on success or failure
def readLineGenerateLogs(reader):
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

#main function
def main():

    #initialize variables based on commandlines or defaults
    fileName = sys.argv[1] if sys.argv[1] else "data"
    ipAddress = sys.argv[2] if sys.argv[2] else "192.168.56.110"

    #these statements set up the syslog handler
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address=(ipAddress, 514))
    logger.addHandler(handler)

    #open file and generate a reader for csv files and close file
    fileObject  = open(fileName, "rb")
    reader = csv.reader(fileObject)

    #makes call to function that generates logs
    readLineGenerateLogs(reader)
    fileObject.close()

if __name__ == "__main__":
  main()


