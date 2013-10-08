#import libraries for parsing
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
from collections import defaultdict
import sys
import re

#class to parse data
class Parser(object):
  def __init__(self):
    ints = Word(nums)
 
    # timestamp of the form <ints>:<ints>:<ints>
    month = Word(string.uppercase, string.lowercase, exact=3)
    day   = ints
    hour  = Combine(ints + ":" + ints + ":" + ints)
    
    timestamp = month + day + hour
 
    # hostname
    hostname = Word(alphas + nums + "_" + "-" + ".")
 
    # appname of the form <Word>[<ints>]:
    appname = Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]")) + Suppress(":")
 
    # message from the logs
    message = Regex(".*")
  
    # pattern build
    self.__pattern = timestamp + hostname + appname + message
    
  def parse(self, line):
    parsed = self.__pattern.parseString(line)

    payload              = {}
    payload["month"]     = parsed[0]
    payload["day"]       = parsed[1]
    payload["time"]      = parsed[2]
    payload["hostname"]  = parsed[3]
    payload["appname"]   = parsed[4]
    payload["pid"]       = parsed[5]
    payload["message"]   = parsed[6]
    
    return payload

def getDataFromMessage(message):
    if "authentication failure" in message:
        #print "Failed"
        username = message.split('=')[-1]
        loginUsers[username] += 1
        #print username
    else:
        print "Passed"
        big_regex = re.compile('|'.join(map(re.escape, unwantedWords)))
        message = big_regex.sub(" ", message)
        #print message
        #matches = re.findall('\w+', message)
        #print matches



#main function
#creates a Parse object, reads the logs line by line
def main():
  parser = Parser()
  global loginUsers
  loginUsers = {}
  loginUsers = defaultdict(int)

  global unwantedWords
  unwantedWords = ["Accepted", "publickey", "for", "from", "port"]

  with open(sys.argv[1]) as syslogFile:
    for line in syslogFile:
      fields = parser.parse(line)
      print fields
      getDataFromMessage(fields["message"])

if __name__ == "__main__":
  main()
