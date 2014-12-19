==================
What is Hacklog?
==================

Hacklog is a security software that detects compromised user accounts 
by applying statistical analysis to service access logs.

Hacklog is implemented as a system deamon that accepts log stream via syslog 
protocol.


http://dandb.github.io/hacklog/

Development
============

[![Build Status](https://travis-ci.org/dandb/hacklog.svg)](https://travis-ci.org/dandb/hacklog)

Clone repository and install the project
```
git clone git@github.com:dandb/hacklog.git
cd hacklog
python setup.py install
python setup.py test
```

Start software
```
cd hacklog/hacklog
./start.sh  # start service
./stop.sh   # stop  service
```

Deployment
==========

Install hacklog package
``yum -y install hacklog``

Start the service 
``service hacklog start``

Point to your syslog output to ``@<hacklog server>``


Community
=========

Mailing list

https://groups.google.com/forum/#!forum/hacklog-devel

https://groups.google.com/forum/#!forum/hacklog-users

Chat 
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/dandb/hacklog?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
