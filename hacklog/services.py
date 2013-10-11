from accessdata import *
from datetime import datetime
import smtplib
from entities import *
import server

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HourRangeEnum = enum(EARLY=range(4), DAWN=range(4,8), MORNING=range(8,12), AFTERNOON=range(12,16), EVE=range(16,20), NIGHT=range(20,24))

class EmailService:

	def __init__(self):
		if server.emailTest:
			gmailUser = 'sshAlertsTest@gmail.com'
			gmailPassword = 'Dandb@123'
			self.mailServer = smtplib.SMTP('smtp.gmail.com', 587)
			self.fromAddress = gmailUser
			self.mailServer.ehlo()
			self.mailServer.starttls()
			self.mailServer.ehlo()
			self.mailServer.login(gmailUser, gmailPassword)
		else:
			self.mailServer = smtplib.SMTP('localhost')
			self.fromAddress = 'sshAlerts@dandb.com'

	def sendMail(self, toAddress, msg):
                msg['From'] = self.fromAddress
		self.mailServer.sendmail(self.fromAddress, toAddress, msg.as_string())

        def sendEmailAlert(self, user, eventLog):
                fromAddress = 'sshAlerts@dandb.com'
                toAddress = 'hackloggroup@googlegroups.com'

                # Create message container - the correct MIME type is multipart/alternative.
                msg = MIMEMultipart()
                msg['Subject'] = "EMAIL ALERT - CONCERNING SSH ACTIVITY ON: " + eventLog.server
                msg['To'] = toAddress

                text = "Hi!\nHow are you?\nThere was some suspicious activity on the following server: " + eventLog.server + " for user: " + user.username + "\n Their current score is " + str(user.score)

                # Record the MIME types of both parts - text/plain and text/html.
                part = MIMEText(text, 'plain')

                msg.attach(part)

                self.sendMail(toAddress, msg)


class UpdateService:

	def __init__(self):
		self._hourRanges = [HourRangeEnum.EARLY, HourRangeEnum.DAWN, HourRangeEnum.MORNING, HourRangeEnum.AFTERNOON, HourRangeEnum.EVE, HourRangeEnum.NIGHT]
		self._rangeName = ['early', 'dawn', 'morning', 'afternoon', 'eve', 'night']
		self._genericDao = GenericDao()
		self._serverDao = ServerDao()
		self._hoursDao = HoursDao()
		self._daysDao = DaysDao()
		self._ipAddressDao = IpAddressDao()
		self._userDao = UserDao()

	def updateAndReturnFreqForProfile(self, profile, value):
		profileDict = profile.profile
		profileDict[value] = profileDict.get(value,0) + 1
		profile.totalCount+=1
		freq = float(profileDict[value])/profile.totalCount
		profile.profile = profileDict
		self._genericDao.mergeEntity(profile)
		return freq

	def updateAndReturnHourFreqForUser(self, eventLog):
		hourProfile = self._hoursDao.getProfileByUser(eventLog.username)
		hour = eventLog.date.hour 
		rangeName = self._rangeName[0]
		for hourRange in self._hourRanges:
			if hour in hourRange:
				rangeName = self._rangeName[self._hourRanges.index(hourRange)]
				break
		if hourProfile == None:
			hourProfile = Hours(eventLog.date, eventLog.username, {}, 0)
			self._genericDao.saveEntity(hourProfile)
		hourFreq = self.updateAndReturnFreqForProfile(hourProfile, rangeName)
		return hourFreq

	def updateAndReturnDayFreqForUser(self, eventLog):
		dayProfile = self._daysDao.getProfileByUser(eventLog.username)
		day = eventLog.date.strftime('%a')
		if dayProfile == None:
			dayProfile = Days(eventLog.date, eventLog.username, {}, 0)
			self._genericDao.saveEntity(dayProfile)
		dayFreq = self.updateAndReturnFreqForProfile(dayProfile, day)
		return dayFreq

	def updateAndReturnServerFreqForUser(self, eventLog):
		serverProfile = self._serverDao.getProfileByUser(eventLog.username)
		if serverProfile == None:
			serverProfile = Servers(eventLog.date, eventLog.username, {}, 0)
			self._genericDao.saveEntity(serverProfile)
		serverFreq = self.updateAndReturnFreqForProfile(serverProfile, eventLog.server)
		return serverFreq

	def updateAndReturnIpFreqForUser(self, eventLog):
		ipProfile = self._ipAddressDao.getProfileByUser(eventLog.username)
		if ipProfile == None:
			ipProfile = IpAddress(eventLog.date, eventLog.username, {}, 0)
			self._genericDao.saveEntity(ipProfile)
		ipFreq = self.updateAndReturnFreqForProfile(ipProfile, eventLog.ipAddress)
		return ipFreq

	def auditEventLog(self, eventLog):
		self._genericDao.saveEntity(eventLog)

	def fetchUser(self, eventLog):
		user = self._userDao.getUserByName(eventLog.username)
		if user == None:
			user = User(eventLog.username, eventLog.date, 0)
			self._genericDao.saveEntity(user)
		return user

	def updateUserScareCount(self, user):
		user.scareCount += 1
		user.lastScareDate = datetime.today()
		self._genericDao.mergeEntity(user)

	def updateUserScore (self, user, score):
		user.score = score
		self._genericDao.mergeEntity(user)

	def resetUserScareCount(self, user):
		user.scareCount = 0
		self._genericDao.mergeEntity(user)
