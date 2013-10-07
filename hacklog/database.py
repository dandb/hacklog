import sqlite3
from sqlalchemy import *

db = create_engine('sqlite:///hacklog.db')

db.echo = True

metadata = BoundMetaData(db)

days = Table('days', metadata, 
	Column('date', DateTime),
	Column('username', String),
	Column('profile', PickleType),)

hours = Table('hours', metadata,
	Column('date', DateTime),
	Column('username', String),
	Column('profile', PickleType),)

servers = Table('servers', metadata,
	Column('date', DateTime),
	Column('username', String),
	Column('profile', PickleType),)

ipAddresses = Table('ip_address', metadata,
		Column('date', DateTime),
		Column('username', String),
		Column('profile', PickleType),)

currentStatus = Table('current_status', metadata,
		Column('username', String),
		Column('date', DateTime),
		Column('score', Integer),)

eventLog = Table('event_log', metadata, 
		Column('date', DateTime),
		Column('username', String),
		Column('ipAddress', String),
		Column('success',),
		Column('server', String),)

metadata.create_all()

dayMapper = mapper(Days, days)
hourMapper = mapper(Hours, hours)
serverMapper = mapper(Servers, servers)
ipAddressesMapper = mapper(IpAddresses, ipAddresses)
currentStatusMapper = mapper(CurrentStatus, currentStatus)
eventLogMapper = mapper(EventLog, eventLog)


