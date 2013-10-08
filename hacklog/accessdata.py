from sqlalchemy.orm import *
from entities import *

class GenericDao:

	def __init__(self):
		self.Session = sessionmaker(db)

	def saveEntity(self, entity):
		session = self.Session()
		session.add(entity)
		session.commit()

class UserDao:
	
	def __init__(self):
		self.Session = sessionmaker(db)

	def getUserByName(self, user):
		session = self.Session()
		fullUser = session.query(User).filter(User.username == user).first()
		return fullUser

class EventLogDao:
	
	def __init__(self):
		self.Session = sessionmaker(db)

class DaysDao:
	
	def __init__(self):
		self.Session = sessionmaker(db)

	def getProfileByUser(self, user):
		session = self.Session()
		days = session.query(Days).filter(Days.username == user).first()
		return days

class HoursDao:
	
	def __init__(self):
		self.Session = sessionmaker(db)

	def getProfileByUser(self, user):
		session = self.Session()
		hours = session.query(Hours).filter(Hours.username == user).first()
		return hours

class IpAddressDao:
	
	def __init__(self):
		self.Session = sessionmaker(db)

	def getProfileByUser(self, user):
		session = self.Session()
		ipAddresses = session.query(IpAddress).filter(IpAddress.username == user).first()
		return ipAddresses

class ServerDao:
	
	def __init__(self):
		self.Session = sessionmaker(db)

	def getProfileByUser(self, user):
		session = self.Session()
		servers = session.query(Servers).filter(Servers.username == user).first()
		return servers
