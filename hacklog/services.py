import accessdata 
from datetime import date


class UpdateService:

	def __init__():
		

	def updateAndReturnHourFreqForUser(eventLog):
		hourProfile = HoursDao.getProfileByUser(eventLog.username)
		hour = 
		hourFreq = updateAndReturnFreqForProfile(hourProfile, hour)
		return hourFreq

	def updateAndReturnDayFreqForUser(eventLog):
		dayProfile = DaysDao.getProfileByUser(eventLog.username)
		day = 
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
