import datetime
import re
import os
import sys

# users
users = dict()

# creates user's object
def create_user(name):
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
def update_dict(dic, key):
 if not key in dic.keys():
   dic[key] = 1
 else:
   dic[key] += 1
 return dic

# pints user category
def print_user_category(cat):
  for key in user[cat].keys():
    print " " + cat + ": " + str(key) + " count: " + str(user[cat][key])

# parse line
def parse_line(logline):
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
    update_user(user_name, user_ip, True, dt_str, host)
    return True

  # failed login
  m = re.match('pam_unix\(sshd:auth\):\s+authentication\s+failure\;\s+login=\s+uid=0\s+euid=0\s+tty=ssh+\s+ruser=+\s+rhost=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+user=([0-9a-zA-Z_-]+)', log_entry)
  if m:
    user_ip = m.groups(0)[0]
    user_name = m.groups(0)[1]
    update_user(user_name, user_ip, False, dt_str, host)
    return True


def update_user(user_name, user_ip, is_login_ok, dt_str, host):

    # add year and parse a datetime string
    dt_str = '2013 ' + dt_str
    dt = datetime.datetime.strptime(dt_str, "%Y %b %d %H:%M:%S")

    # create user
    if not user_name in users.keys():
      user = create_user(user_name)
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
    user['hour'] = update_dict(user['hour'], dt.hour)
    # increate Fq for Day of the week
    user['day'] = update_dict(user['day'], dt.strftime('%a'))
    # increate Fq in  Month
    user['month'] = update_dict(user['month'], dt.strftime('%b'))

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

# go over logs
#for host in os.listdir("logs"):
#  if os.path.isfile("logs/" + host + "/secure"):
#    log = open( "logs/" + host + "/secure", "r" )
with open(sys.argv[1]) as syslogFile:
    for line in syslogFile:
        if line:
            parse_line(line)

# print info for all users
for user in users.keys():

  user = users[user]
  ip_count = 0

  for ip in user['ip'].keys():
    ip_count += 1

  print "User: " + user['name'] + " Successful login count = " + str(user['ok']) + " Failed login count " + str(user['fail'])
  for cat in ['month','day','hour','ip']:
    print_user_category(cat)
