from sqlalchemy.orm import *
from entities import *
from session import Session

class GenericDao:

	def saveEntity(self, entity):
		session = Session()
		session.add(entity)
		session.commit()

	def mergeEntity(self, entity):
		session = Session()
		session.merge(entity)
		session.commit()

class UserDao:
	
	def getUserByName(self, user):
		session = Session()
		fullUser = session.query(User).filter(User.username == user).first()
		return fullUser

class DaysDao:
	
	def getProfileByUser(self, user):
		session = Session()
		days = session.query(Days).filter(Days.username == user).first()
		return days

class HoursDao:
	
	def getProfileByUser(self, user):
		session = Session()
		hours = session.query(Hours).filter(Hours.username == user).first()
		return hours

class IpAddressDao:
	
	def getProfileByUser(self, user):
		session = Session()
		ipAddresses = session.query(IpAddress).filter(IpAddress.username == user).first()
		return ipAddresses

class ServerDao:
	
	def getProfileByUser(self, user):
		session = Session()
		servers = session.query(Servers).filter(Servers.username == user).first()
		return servers
