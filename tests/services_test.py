import unittest
from mockito import mock, when, verify, any
import sys
sys.path.append('../hacklog')
from entities import *
from services import *
import re
from datetime import datetime

emailService = EmailService()
updateService = UpdateService()

class ServiceTests(unittest.TestCase):

    def setUp(self):
	self._eventLog = EventLog(datetime.now(), 'nrhine', '1.2.3.4', True, 'prod')
	self._user = User('nrhine', datetime.now(), 10)
	self._day = Days(datetime.now(), 'nrhine', {'1.2.3.5':1}, 1 )
	self._hour = Hours(datetime.now(), 'nrhine', {}, 0)
	self._server = Servers(datetime.now(), 'nrhine', {}, 0)
	self._ipAddr = IpAddress(datetime.now(), 'nrhine', {}, 0)
	updateService._genericDao = mock()
	updateService._userDao = mock()
	updateService._daysDao = mock()
	updateService._hoursDao = mock()
	updateService._serversDao = mock()
	updateService._ipAddressDao = mock()
	emailService._smtpSend = mock()

    def test_email_send(self):
	emailService.sendEmailAlert(self._user, self._eventLog)
	when(emailService._smtpSend).sendmail(any())
	verify(emailService._smtpSend, times=1).sendmail(any())

    def test_update_day_new_user(self):
	when(updateService._daysDao).getProfileByUser(self._eventLog.username).thenReturn(None)
	freq = updateService.updateAndReturnDayFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_update_day_old_user(self):
	when(updateService._daysDao).getProfileByUser(self._eventLog.username).thenReturn(self._day)
	freq = updateService.updateAndReturnDayFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_update_hour_new_user(self):
	when(updateService._hoursDao).getProfileByUser(self._eventLog.username).thenReturn(None)
	freq = updateService.updateAndReturnHourFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_update_hour_old_user(self):
	when(updateService._hoursDao).getProfileByUser(self._eventLog.username).thenReturn(self._hour)
	freq = updateService.updateAndReturnHourFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_update_server_new_user(self):
	when(updateService._serverDao).getProfileByUser(self._eventLog.username).thenReturn(None)
	freq = updateService.updateAndReturnServerFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_update_server_old_user(self):
	when(updateService._daysDao).getProfileByUser(self._eventLog.username).thenReturn(self._server)
	freq = updateService.updateAndReturnServerFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_update_ipAddr_new_user(self):
	when(updateService._ipAddressDao).getProfileByUser(self._eventLog.username).thenReturn(None)
	freq = updateService.updateAndReturnIpFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_update_ipAddr_old_user(self):
	when(updateService._ipAddressDao).getProfileByUser(self._eventLog.username).thenReturn(self._ipAddr)
	freq = updateService.updateAndReturnIpFreqForUser(self._eventLog)
	self.assertIsInstance(freq, float)

    def test_fetch_user_no_existing(self):
	when(updateService._userDao).getUserByName(self._eventLog.username).thenReturn(None)
	user = updateService.fetchUser(self._eventLog)
	self.assertIsInstance(user, User)

    def test_fetch_user_existing(self):
	when(updateService._userDao).getUserByName(self._eventLog.username).thenReturn(self._user)
	user = updateService.fetchUser(self._eventLog)
	self.assertIsInstance(user, User)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

