import sqlite3
from hacklog.entities import DayProfile,HourProfile,ServerProfile,IpAddressProfile


def __init__():
	self._conn=sqlite3.connect('hacklog.db')

def initialize_profile():
	sqlite3.register_adapter(Profile, adapt_profile)
	sqlite3.register_converter(Profile, convert_profile)

def initialize_day_table():
	self._conn.execute("create table day(datetime text, user text, profile Profile)

def initialize_hour_table():
	self._conn.execute("create table hour(datetime text, user text, profile Profile)

def initialize_server_table():
	self._conn.execute("create table server(datetime text, user text, profile Profile)

def initialize_ip_address_table():
	self._conn.execute("create table ip_address(datetime text, user text, profile Profile)
	
def initialize_current_status_table():
	self._conn.execute("create table current_status(user_text PRIMARY KEY, datetime text, current_score int)

def initialize_event_log_table():
	self._conn.execute("create table event_log(datetime text, user text, ip_address text, success int, server text)

