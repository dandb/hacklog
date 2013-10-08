import accessdata 
from datetime import date
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Hours = enum(EARLY=range(4), DAWN=range(4,8), MORNING=range(8-12), AFTERNOON=range(12-16), EVE=range(16-20), NIGHT=range(20-24))

class EmailService:

        def sendEmailAlert(user, eventLog)
                from = "sshAlerts@dandb.com"
                to = "nrhine@dandb.com"

                # Create message container - the correct MIME type is multipart/alternative.
                msg = MIMEMultipart('alternative')
                msg['Subject'] = "EMAIL ALERT - CONCERNING SSH ACTIVITY ON: " + eventLog.server
                msg['From'] = from
                msg['To'] = to

                text = "Hi!\nHow are you?\nThere was some suspicious activity on the following server: " + eventLog.server + " for user: " + user.username + "\n Their current score is " + user.score

                # Record the MIME types of both parts - text/plain and text/html.
                part = MIMEText(text, 'plain')

                msg.attach(part)

                s = smtplib.SMTP('localhost')
                s.sendmail(from, to, msg.as_string())
                s.quit()


class UpdateService:

	def __init__():
		self._hourRanges = [Hours.EARLY, Hours.DAWN, Hours.MORNING, Hours.AFTEROON, Hours.EVE, Hours.NIGHT]
		self._rangeName = ['early', 'dawn', 'morning', 'afternoon', 'eve', 'night']

	def updateAndReturnHourFreqForUser(eventLog):
		hourProfile = HoursDao.getProfileByUser(eventLog.username)
		hour = eventLog.date.hour 
		rangeName = self._rangeName[0]
		for hourRange in self._hourRanges:
			if hour is in hourRange
				rangeName = self._rangeName[_self.hourRanges.index(hourRange)
		
		hourFreq = updateAndReturnFreqForProfile(hourProfile, rangeName)
		return hourFreq

	def updateAndReturnDayFreqForUser(eventLog):
		dayProfile = DaysDao.getProfileByUser(eventLog.username)
		day = eventLog.date.strftime('%a')
		dayFreq = updateAndReturnFreqForProfile(dayProfile, day)
		return dayFreq

	def updateAndReturnServerFreqForUser(eventLog):
		serverProfile = ServerDao.getProfileByUser(eventLog.username)
		serverFreq = updateAndReturnFreqForProfile(serverProfile, eventLog.server)
		return serverFreq

	def updateAndReturnIpFreqForUser(eventLog):
		ipProfile = IpAddressDao.getProfileByUser(eventLog.username)
		ipFreq = updateAndReturnFreqForProfile(ipProfile, eventLog.ipAddress)
		return ipFreq

	def updateAndReturnFreqForProfile(profile, value):
		profileDict = profile.profile
		profileDict[value] = profileDict.get(value,0) + 1
		profile.totalCount+=1
		freq = profileDict[value]/profile.totalCount
		GenericDAO.saveEntity(profile)
		return freq

	def auditEventLog(eventLog):
		GenericDAO.saveEntity(eventLog)

	def updateUserScore(score, eventLog):
		user = UserDao.getUserByName(eventLog.username)
		user.score = score
		GenericDAO.saveEntity(user)
		return user

	def updateUserScareCount(user):
		user.scareCount += 1
		user.lastScareDate = date.today()
		GenericDAO.saveEntity(user)
