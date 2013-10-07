
class EventLog:
	def __init__(self, date, username, ipAddress, success, server):
		self._date = date
		self._username = username
		self._ipAddress = ipAddress
		self._success = success
		self._server = server

	def convert_for_sqlite():
		return (self._date, self._username, self._ipAddress, self._success, self._server)

class CurrentStatus:
	def __init__(self, username, date, score):
		self._username=username
		self._date=date
		self._score=score

	def convert_for_sqlite():
		return (self._username, self._date, self._score,)

class Profile:

	def __init__(self, profileDict):
		self._profileDict = profileDict
	
	def adapt_profile():
		profile=""
		first=True
		for key in self._profileDict.keys():
			if first:
				first = False
				profile = "%s:%d" % (key, self._profileDict[key])
			else:
				profile += ";%s:%d" % (key, self._profileDict[key])
		return profile

	def convert_profile(s):
		splitList = s.split(";")
		profile={}
		for element in splitList
			element,value = s.split(":")
			profile[element] = value
		return Profile(profile)


class Day:
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile
	
	def convert_for_sqlite():
		return (self._date, self._username, self._profile,);
	

class Hour:
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile
	
	def convert_for_sqlite():
		return (self._date, self._username, self._profile,);


class Server:
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile
	
	def convert_for_sqlite():
		return (self._date, self._username, self._profile,);

class IpAddress:
	def __init__(self, date, username, profile):
		self._date=date
		self._username=username
		self._profile = profile
	
	def convert_for_sqlite():
		return (self._date, self._username, self._profile,);
