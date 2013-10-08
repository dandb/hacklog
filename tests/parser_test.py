import unittest
import sys
sys.path.append('../hacklog')
from parse import Parser
import re

class ParserTests(unittest.TestCase):

    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_parse_line(self):
        self.assertIsInstance(Parser.parse_line("Oct  4 17:57:37 192.168.56.1 sshd[1690]: Accepted publickey for mvalenzuela from 10.42.28.22 port 7786 ssh2"), EventLog)

    #def test_regex_login_match(self):
     #   self.assertEquals(regex_login_match("Accepted publickey for mvalenzuela from 10.42.28.22 port 7786 ssh2"), True)

    #def test_regex_login_fail_match(self):
    #    self.assertEquals(regex_login_fail_match("pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=10.42.10.22 user=msacks"), True)

    #def test_file_opens(self):
    #    self.assertTrue(file_present(file_name), None)

def main():
    #global file_name
    #file_name = sys.argv[1:]
    #del sys.argv[1:]
    unittest.main()

if __name__ == "__main__":
    main()

