import unittest
import sys
from hacklog import Parser
import re

def parse_line_length(data):
    data = data.split(' ')
    if len(data) > 5:
        return True

def regex_login_match(data):
    m = re.match('Accepted\s+publickey\s+for\s+([0-9a-zA-Z_-]+)\s+from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+port', data)
    return True

def regex_login_fail_match(data):
    m = re.match('pam_unix\(sshd:auth\):\s+authentication\s+failure\;\s+login=\s+uid=0\s+euid=0\s+tty=ssh+\s+ruser=+\s+rhost=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+user=([0-9a-zA-Z_-]+)', data)
    return True

def file_present(file):
    if file:
        return True

class CSVFileTests(unittest.TestCase):

    def test_starting_out(self):
        self.assertEqual(1, 1)

    def test_parse_line_length(self):
        self.assertEquals(Parser.parse_line("Oct  4 17:57:37 192.168.56.1 sshd[1690]: Accepted publickey for mvalenzuela from 10.42.28.22 port 7786 ssh2"), True)

    #def test_regex_login_match(self):
     #   self.assertEquals(regex_login_match("Accepted publickey for mvalenzuela from 10.42.28.22 port 7786 ssh2"), True)

    #def test_regex_login_fail_match(self):
    #    self.assertEquals(regex_login_fail_match("pam_unix(sshd:auth): authentication failure; login= uid=0 euid=0 tty=ssh ruser= rhost=10.42.10.22 user=msacks"), True)

    #def test_file_opens(self):
    #    self.assertTrue(file_present(file_name), None)

def main():
    global file_name
    file_name = sys.argv[1:]
    del sys.argv[1:]
    unittest.main()

if __name__ == "__main__":
    main()

