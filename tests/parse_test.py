import unittest
import sys
sys.path.append('../hacklog')
from parse import Parser
from entities import *
import re

parse = Parser()

class ParserTests(unittest.TestCase):

    #parse = Parser()
    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_parse_line_success(self):
        sysLogMessage = SyslogMsg("<14>sshd[3070]: Accepted publickey for kantselovich from 10.42.10.2 port 2005 ssh2\x00", "192.168.56.1")
        self.assertIsInstance(parse.parseLogLine(sysLogMessage), EventLog)

    def test_parse_line_failure(self):
        sysLogMessage = SyslogMsg("<14>sshd[3070]: pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=10.42.10.22 user=msacks", "192.168.56.1")
        self.assertIsInstance(parse.parseLogLine(sysLogMessage), EventLog)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

