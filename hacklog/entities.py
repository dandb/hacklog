from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

db = create_engine('sqlite:///hacklog.db', echo=True)
Base = declarative_base()

class EventLog(Base):
	__tablename__ = 'eventLog'

	date = Column('date', DateTime, primary_key=True)
	username = Column('username', String, primary_key=True)
	ipAddress = Column('ipAddress', String)
	success = Column('success', Boolean)
	server = Column('server', String)	

	def __init__(self, date, username, ipAddress, success, server):
		self.date = date
		self.username = username
		self.ipAddress = ipAddress
		self.success = success
		self.server = server

class User(Base):
	__tablename__ = 'users'	
	
	username = Column('username', String, primary_key=True)
	date = Column('date', DateTime)
	score = Column('score', Integer)
	scareCount = Column('scareCount', Integer)
	lastScareDate = Column('lastScareDate', DateTime)

	def __init__(self, username, date, score):
		self.username=username
		self.date=date
		self.score=score
		self.scareCount=0
		self.lastScareDate = date.today()

class Days(Base):
	__tablename__ = 'days'

	date = Column('date', DateTime, primary_key=True)
        username = Column('username', String, primary_key=True)
        profile = Column('profile', PickleType)
        totalCount = Column('totalCount', Integer)

	def __init__(self, date, username, profile, totalCount):
		self.date=date
		self.username=username
		self.profile = profile
		self.totalCount = totalCount
	
class Hours(Base):
	__tablename__ = 'hours'

	date = Column('date', DateTime, primary_key=True)
        username = Column('username', String, primary_key=True)
        profile = Column('profile', PickleType)
        totalCount = Column('totalCount', Integer)

	def __init__(self, date, username, profile, totalCount):
		self.date=date
		self.username=username
		self.profile = profile
		self.totalCount = totalCount

class Servers(Base):
	__tablename__ = 'servers'

	date = Column('date', DateTime, primary_key=True)
        username = Column('username', String, primary_key=True)
        profile = Column('profile', PickleType)
        totalCount = Column('totalCount', Integer)

	def __init__(self, date, username, profile, totalCount):
		self.date=date
		self.username=username
		self.profile = profile
		self.totalCount = totalCount

class IpAddress(Base):
	__tablename__ = 'ipAddress'

	date = Column('date', DateTime, primary_key=True)
        username = Column('username', String, primary_key=True)
        profile = Column('profile', PickleType)
        totalCount = Column('totalCount', Integer)

	def __init__(self, date, username, profile, totalCount):
		self.date=date
		self.username=username
		self.profile = profile
		self.totalCount = totalCount

class SyslogMsg():

   def __init__(self, data='', host='', port=0):
     self.data = data
     self.host = host
     self.port = port
     self.date = datetime.now()

def create_tables():
        Base.metadata.create_all(db)

def enum(**enums):
	return type('Enum', (), enums)

Days= enum(MON='monday', TUES='tuesday', WED='wednesday', THURS='thursday', FRI='friday', SAT='saturday', SUN='sunday')
Hours = enum(EARLY=range(4), DAWN=range(4,8), MORNING=range(8-12), AFTERNOON=range(12-16), EVE=range(16-20), NIGHT=range(20-24))
Weight = enum(HOURS=10, DAYS=10, SERVER=15, SUCCESS=35, VPN=10, INT=10, IP=10)
