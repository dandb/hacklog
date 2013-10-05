from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
 
class Parser(object):
  def __init__(self):
    ints = Word(nums)
 
    # priority
    priority = Suppress("<") + ints + Suppress(">")
 
    # timestamp
    month = Word(string.uppercase, string.lowercase, exact=3)
    day   = ints
    hour  = Combine(ints + ":" + ints + ":" + ints)
    
    timestamp = month + day + hour
 
    # hostname
    hostname = Word(alphas + nums + "_" + "-" + ".")
 
    # appname
    appname = Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]")) + Suppress(":")
 
    # message
    message = Regex(".*")
  
    # pattern build
    self.__pattern = priority + timestamp + hostname + appname + message
    
  def parse(self, line):
    parsed = self.__pattern.parseString(line)
 
    payload              = {}
    payload["priority"]  = parsed[0]
    payload["timestamp"] = strftime("%Y-%m-%d %H:%M:%S")
    payload["hostname"]  = parsed[4]
    payload["appname"]   = parsed[5]
    payload["pid"]       = parsed[6]
    payload["message"]   = parsed[7]
    
    return payload
 
""" --------------------------------- """
 
def main():
  parser = Parser()
  
  with open('./logs.csv') as syslogFile:
    for line in syslogFile:
      fields = parser.parse(line)
      print "parsed:", fields
  
if __name__ == "__main__":
  main()
