from entities import EventLog
from datetime import datetime
import re

class Parser():
  def __init__(self, successPattern=None, failurePattern=None):
    self.successPattern = successPattern or 'Accepted\s+publickey\s+for\s+([0-9a-zA-Z_-]+)\s+from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+port'
    self.failurePattern = failurePattern or 'pam_unix\(sshd:auth\):\s+authentication\s+failure\;\s+login=\s+uid=0\s+euid=0\s+tty=ssh+\s+ruser=+\s+rhost=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+user=([0-9a-zA-Z_-]+)'

  def parseLogLine(self, line):

    logline = re.sub('\s{2,}', ' ', line)
    logline = logline.split(' ')

    if len(logline) < 5:
      return True

    dt_str = logline.pop(0) + ' ' + logline.pop(0) + ' ' + logline.pop(0)
    host = logline.pop(0)
    prog = logline.pop(0).split(':')[0]
    log_entry = ' '.join(logline)

    # successful login
    m = re.match(self.successPattern, log_entry)
    if m:
      user_name = m.groups(0)[0]
      user_ip = m.groups(0)[1]
      return EventLog(datetime.now(), user_name, user_ip, True, host)
    # successful login
    m = re.match(self.failurePattern, log_entry)
    if m:
      user_name = m.groups(0)[0]
      user_ip = m.groups(0)[1]
      return EventLog(datetime.now(), user_name, user_ip, False, host)
    
