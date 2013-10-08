from sqlalchemy import *

class GenericDao:

	def __init__():
		self.Session = sessionmaker(db)

	def saveEntity(entity):
		session = self.Session()
		session.add(entity)
		session.commit()

class UserDao:
	
	def __init__():
		self.Session = sessionmaker(db)

	def getUserByName(user)
		session = self.Session()
		fullUser = session.query(Users).filter(Users.username == user).first()
		return fullUser

class EventLogDao:
	
	def __init__():
		self.Session = sessionmaker(db)

class DaysDao:
	
	def __init__():
		self.Session = sessionmaker(db)

	def getProfileByUser(user):
		session = self.Session()
		days = session.query(Days).filter(Days.username == user).first()
		return days

class HoursDao:
	
	def __init__():
		self.Session = sessionmaker(db)

	def getProfileByUser(user):
		session = self.Session()
		hours = session.query(Hours).filter(Hours.username == user).first()
		return hours

class IpAddressDao:
	
	def __init__():
		self.Session = sessionmaker(db)

	def getProfileByUser(user):
		session = self.Session()
		ipAddresses = session.query(IpAddress).filter(IpAddress.username == user).first()
		return ipAddresses

class ServerDao:
	
	def __init__():
		self.Session = sessionmaker(db)

	def getProfileByUser(user):
		session = self.Session()
		servers = session.query(Servers).filter(Servers.username == user).first()
		return servers
