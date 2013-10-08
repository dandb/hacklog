import datetime
import re
import os
import sys

# users
users = dict()

class Parser(object):

    # creates user's object
    def create_user(self, name):
        user = dict()
        user['name'] = name
        user['ip'] = dict()
        user['ok'] = 0
        user['fail'] = 0
        user['month'] = dict()
        user['day'] = dict()
        user['hour'] = dict()
        return user

    # updates or creates key in dict
    def update_dict(self, dic, key):
        if not key in dic.keys():
            dic[key] = 1
        else:
            dic[key] += 1
        return dic

    # pints user category
    def print_user_category(self, user, cat):
        for key in user[cat].keys():
            print " " + cat + ": " + str(key) + " count: " + str(user[cat][key])

    # parse line
    def parse_line(self, logline):
        logline = re.sub('\s{2,}', ' ', logline)
        logline = logline.split(' ')

        if len(logline) < 5:
            return True

        dt_str = logline.pop(0) + ' ' + logline.pop(0) + ' ' + logline.pop(0)
        host = logline.pop(0)
        prog = logline.pop(0).split(':')[0]
        log_entry = ' '.join(logline)

        # successful login
        m = re.match('Accepted\s+publickey\s+for\s+([0-9a-zA-Z_-]+)\s+from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+port', log_entry)
        if m:
            user_name = m.groups(0)[0]
            user_ip = m.groups(0)[1]
            self.update_user(user_name, user_ip, True, dt_str, host)
            return True

        # failed login
        m = re.match('pam_unix\(sshd:auth\):\s+authentication\s+failure\;\s+login=\s+uid=0\s+euid=0\s+tty=ssh+\s+ruser=+\s+rhost=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+user=([0-9a-zA-Z_-]+)', log_entry)
        if m:
            user_ip = m.groups(0)[0]
            user_name = m.groups(0)[1]
            self.update_user(user_name, user_ip, False, dt_str, host)
            return True


    def update_user(self, user_name, user_ip, is_login_ok, dt_str, host):

        # add year and parse a datetime string
        dt_str = '2013 ' + dt_str
        dt = datetime.datetime.strptime(dt_str, "%Y %b %d %H:%M:%S")

        # create user
        if not user_name in users.keys():
          user = self.create_user(user_name)
        else:
          user = users[user_name]

        # increate Fq for IP
        if not user_ip in user['ip'].keys():
          user['ip'][user_ip] = 1
        else:
          user['ip'][user_ip] += 1

        # increate successful login Fq
        if is_login_ok:
          user['ok'] += 1
        else:
          user['fail'] += 1

        # increate Fq for Hour of the day
        user['hour'] = self.update_dict(user['hour'], dt.hour)
        # increate Fq for Day of the week
        user['day'] = self.update_dict(user['day'], dt.strftime('%a'))
        # increate Fq in  Month
        user['month'] = self.update_dict(user['month'], dt.strftime('%b'))

        # save user
        users[user_name] = user

        # outut CSV
        line = [];
        line.append( dt.strftime("%Y-%m-%d %H:%M:%S") )
        line.append( user_name )
        line.append( user_ip )
        line.append( str(is_login_ok) )
        line.append( host )

        return True

def main():

    #initiate the object of class
    parser = Parser()

    # go over logs
    fileName = sys.argv[1] if sys.argv[1] else "syslog"

    with open(fileName) as syslogFile:
        for line in syslogFile:
            if line:
                parser.parse_line(line)

    # print info for all users
    for user in users.keys():
      user = users[user]
      ip_count = 0

      for ip in user['ip'].keys():
        ip_count += 1

      print "User: " + user['name'] + " Successful login count = " + str(user['ok']) + " Failed login count " + str(user['fail'])
      for cat in ['month','day','hour','ip']:
        parser.print_user_category(user, cat)

if __name__ == "__main__":
  main()