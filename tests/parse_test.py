import unittest
import sys
sys.path.append('../hacklog')
from parse import Parser
from entities import EventLog
import re

parse = Parser()

class ParserTests(unittest.TestCase):

    #parse = Parser()
    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_parse_line_success(self):
        self.assertIsInstance(parse.parseLogLine("Oct  4 17:57:37 192.168.56.1 sshd[1690]: Accepted publickey for mvalenzuela from 10.42.28.22 port 7786 ssh2"), EventLog)

    def test_parse_line_failure(self):
        self.assertIsInstance(parse.parseLogLine("Oct  4 17:57:37 192.168.56.1 ssshd[6520]: pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=10.42.10.22 user=msacks"), EventLog)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

