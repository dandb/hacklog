import sys
import datetime 
import time
import thread
import random

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from optparse import OptionParser
from ConfigParser import ConfigParser

class SyslogServer():
    """
    Syslog server based on twisted library
    """

    def __init__(self):
      self.port = 10514
      self.bind_address = '127.0.0.1'
      self.config_file = './server.conf'

    def parceConfig(self, config_file):
       config = ConfigParser()
       config.read(config_file)
        
       if config.has_option('SyslogServer', 'bind_address'):
         self.bind_address = config.get('SyslogServer', 'bind_address')
       if config.has_option('SyslogServer', 'bind_port'):
         self.port = config.getint('SyslogServer', 'port')       

    def run(self):
      reactor.listenUDP(self.port, ReadSyslog())
      reactor.run() 

    def stop(self):
      reactor.stop()


class ReadSyslog(DatagramProtocol):

    def parceMessage(self, data, host, port):
        delay = random.random()
        time.sleep(delay)
        print "sleeped for " + str(delay) + " in thread " + str(thread.get_ident()) + " received %r from %s:%d" % (data, host, port)
#       self.transport.write(data, (host, port))

    def datagramReceived(self, data, (host, port)):
        reactor.callInThread(self.parceMessage, data, host, port)

def main():
    usage = "usage: %prog -c config_file"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", dest="config_file",
                      help="configuration file", metavar="FILE")
    (options, args) = parser.parse_args()
    if not options.config_file:
        parser.error('you must specify a configuration file')

    server = SyslogServer()
    server.parceConfig(options.config_file)

    server.run()

if __name__ == '__main__':
    main()
