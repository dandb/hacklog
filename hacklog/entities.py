from sqlalchemy import Column, Integer, String


class EventLog(object):
	def __init__(self, date, username, ipAddress, success, server):
		self._date = date
		self._username = username
		self._ipAddress = ipAddress
		self._success = success
		self._server = server

class CurrentStatus(object):
	def __init__(self, username, date, score):
		self._username=username
		self._date=date
		self._score=score

class Day(object):
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile
	
class Hour(object):
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile

class Server(object):
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile

class IpAddress(object):
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile
	
