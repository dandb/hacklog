import enitities
from math import log

Weight = enum(HOURS=10, DAYS=10, SERVER=15, SUCCESS=35, VPN=0, INT=10, EXT=15, IP=15)
Threshold = enum(CRITICAL=50, SCARY=30, SCARECOUNT=3)

def processEventLog(eventLog)
	auditEventLog(eventLog)
	user = calculateNewScore(eventLog)
	if user.score > Threshold.CRITICAL
		processAlert(user)
	elif user.score > Threshold.SCARY
		if user.scareCount >= Threshold.SCARECOUNT
			processAlert(user)
		UpdateService.updateScareCount(user)

def calculateNewScore(eventLog)
	successScore = calculateSuccessScore(eventLog.success)
	ipLocationScore = calculateIpLocationScore(eventLog.ipAddress)

	serverScore = calculateServerScore(eventLog)
	ipScore = calculateIpScore(eventLog)
	dayScore = calculateDayScore(eventLog)
	hourScore = calculateHourScore(eventLog)
	
	totalScore = successScore + ipLocationScore + serverScore + ipScore + dayScore + hourScore
	
	user = UpdateService.updateUserScore(totalScore, eventLog)

def auditEventLog(eventLog)
	UpdateService.auditEventLog(eventLog)

def calculateHoursScore(eventLog):
	hourFreq = UpdateService.updateAndReturnHourFreqForUser(eventLog)
	hourScore = calculateSubscore(hourFreq)*Weight.HOURS

def calculateDaysScore(eventLog):
	dayFreq = UpdateService.updateAndReturnDayFreqForUser(eventLog)
	dayScore = calculateSubscore(dayFreq)*Weight.DAYS

def calculateServerScore(eventLog):
	serverFreq = UpdateService.updateAndReturnServerFreqForUser(eventLog)
	serverScore = calculateSubscore(serverFreq) * Weight.SERVER

def calculateIpScore(eventLog):
	ipFreq = UpdateService.updateAndReturnIpFreqForUser(eventLog)
	ipScore = calculateSubscore(ipFreq) * Weight.IP


def calculateSubscore(freq)
	subscore = math.log(freq, 2)
	subscore = subscore*-10
	if(subscore>100)
		return 100
	return subscore

def calculateSuccessScore(success)
	successScore = Weight.SUCCESS
	if success
		successScore = 0
	return successScore

def calculateIpLocationScore(ipAddress)
	ipScore = Weight.EXT
	if IpAddress.checkIpForVpn(ipAddress)
		ipScore=Weight.VPN
	if IpAddress.checkIpForInternal(ipAddress)
		ipScore=Weight.INT
	return ipScore
