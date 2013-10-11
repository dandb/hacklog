from entities import EventLog
from entities import SyslogMsg
from datetime import datetime
import re

class Parser():
  def __init__(self, successPattern=None, failurePattern=None, successDateTimePatten=None, failureDateTimePattern=None):
    self.successPattern = successPattern or 'Accepted\s+publickey\s+for\s+([0-9a-zA-Z_-]+)\s+from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+port'
    self.failurePattern = failurePattern or 'pam_unix\(sshd:auth\):\s+authentication\s+failure\;\s+login=\s+uid=0\s+euid=0\s+tty=ssh+\s+ruser=+\s+rhost=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+user=([0-9a-zA-Z_-]+)'
    self.successDateTimePatten = successDateTimePatten or 'Accepted\s+publickey\s+for\s+([0-9a-zA-Z_-]+)\s+from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+port\s+(\d{1,4})+\s+ssh2+\s+DATE_TIME\s+(\d{1,4}-\d{1,2}-\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+HOST\s+([\w\+%\-& ]+)'
    self.failureDateTimePattern = failureDateTimePattern or 'pam_unix\(sshd:auth\):\s+authentication\s+failure\;\s+login=\s+uid=0\s+euid=0\s+tty=ssh+\s+ruser=+\s+rhost=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+user=([0-9a-zA-Z_-]+)\s+DATE_TIME\s+(\d{1,4}-\d{1,2}-\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+HOST\s+([\w\+%\-& ]+)'
  def parseLogLine(self, message):

    returnEvent = False

    if message:
        line = message.data
        host = message.host
        logline = re.sub('\s{2,}', ' ', line)

        if "Source Network Address" not in line and "Account Name:" not in line:
            logline = logline.split(' ')
            if len(logline) > 5:
                logline.pop(0)
                log_entry = ' '.join(logline)
                # successful login
                m = re.match(self.successDateTimePatten, log_entry)
                if m:
                    user_name = m.groups(0)[0]
                    user_ip = m.groups(0)[1]
                    date_time = m.groups(0)[3]
                    date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    host = m.groups(0)[4]
                    returnEvent = EventLog(date_time, user_name, user_ip, True, host)

                # login failed
                m = re.match(self.failureDateTimePattern, log_entry)
                if m:
                    user_name = m.groups(0)[1]
                    user_ip = m.groups(0)[0]
                    date_time = m.groups(0)[2]
                    date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    host = m.groups(0)[3]
                    returnEvent = EventLog(date_time, user_name, user_ip, False, host)
        elif "Source Network Address" in line and "Account Name:" in line:
            userIP = logline.split("Source Network Address:")
            userIP = userIP[1].lstrip()
            user_ip = userIP[0:userIP.index(" ")].rstrip()
            accountName = logline.split("Account Name:")
            if logline.count("Account Name:") > 1:
                accountName = accountName[2]
            else:
                accountName = accountName[1]
            userName = accountName.lstrip()
            user_name = userName[0:userName.index(" ")].rstrip()
            returnEvent = EventLog(datetime.now(), user_name, user_ip, True, host)
        else:
            returnEvent = False
    else:
        returnEvent = False

    if returnEvent:
        return returnEvent
    else:
        return None



