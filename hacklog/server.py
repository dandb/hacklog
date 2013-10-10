import sys
import time
import thread
import random
import algorithm
import signal

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer

from optparse import OptionParser
from ConfigParser import ConfigParser
from parse import Parser
from entities import SyslogMsg
from Queue import Queue
from entities import create_tables

queue = Queue()
parser = Parser()

class SyslogServer():
    """
    Syslog server based on twisted library
    """

    def __init__(self):
      self.port = 10514
      self.bind_address = '127.0.0.1'
      self.config_file = './server.conf'
      self.debug = 10
      self.running = True

    def parceConfig(self, config_file):
       config = ConfigParser()
       config.read(config_file)
        
       if config.has_option('SyslogServer', 'bind_address'):
         self.bind_address = config.get('SyslogServer', 'bind_address')
       if config.has_option('SyslogServer', 'bind_port'):
         self.port = config.getint('SyslogServer', 'port')       
    

    def interrupt(self, signum, stackframe):
      print "Got signal: %s" % signum
      self.running = False
      queue.put(SyslogMsg())
      self.stop()
 
    def messageParcer(self):

       if self.debug <= 10:
          print "messageParcer in thread " + str(thread.get_ident())

       while self.running:
          msg = queue.get()
          delay = random.random()
	  eventLog = parser.parseLogLine(msg)
	  if eventLog:
	      algorithm.processEventLog(eventLog)
              time.sleep(delay)
              print "messages in queue " + str(queue.qsize()) + ",sleeped for " + str(delay) + ", received %r from %s:%d" % (msg.data, msg.host, msg.port)
    
    def cleanupThread(self):
      threadPool = reactor.getThreadPool()
      threadPool.stop()

    def run(self):
      signal.signal(signal.SIGINT, self.interrupt)
      reactor.callInThread(self.messageParcer)
      reactor.listenUDP(self.port, SyslogReader())
      reactor.run()

    def stop(self):
      reactor.stop()


class SyslogReader(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        syslogMsg = SyslogMsg(data, host, port)
        queue.put(syslogMsg)

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
    create_tables()

    server.run()

if __name__ == '__main__':
    main()
