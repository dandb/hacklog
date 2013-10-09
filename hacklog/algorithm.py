import services
from entities import EventLog
from entities import enum
from entities import IpAddress
import math
from datetime import date

Weight = enum(HOURS=10, DAYS=10, SERVER=15, SUCCESS=35, VPN=0, INT=10, EXT=15, IP=15)
Threshold = enum(CRITICAL=50, SCARY=30, SCARECOUNT=3)

updateService = services.UpdateService()

def testProcess():
	eventLog = EventLog(date.today(), 'nrhine', '127.0.0.1', True, 'ae1-app80-prd')
	processEventLog(eventLog)

def processEventLog(eventLog):
	auditEventLog(eventLog)
	score = calculateNewScore(eventLog)
	user = updateService.fetchUser(eventLog)
	if score > Threshold.CRITICAL:
                processAlert(user, eventLog)
        elif score > Threshold.SCARY:
                if user.scareCount >= Threshold.SCARECOUNT:
                        processAlert(user, eventLog)
                user = updateService.updateScareCount(user)

def calculateNewScore(eventLog):
	successScore = calculateSuccessScore(eventLog.success)
	ipLocationScore = calculateIpLocationScore(eventLog.ipAddress)

	serverScore = calculateServerScore(eventLog)
	ipScore = calculateIpScore(eventLog)
	dayScore = calculateDaysScore(eventLog)
	hourScore = calculateHoursScore(eventLog)
	
	totalScore = successScore + ipLocationScore + serverScore + ipScore + dayScore + hourScore
	
	return totalScore

def auditEventLog(eventLog):
	updateService.auditEventLog(eventLog)

def processAlert(user, eventLog):
	EmailService.sendEmailAlert(user, eventLog)

def calculateHoursScore(eventLog):
	hourFreq = updateService.updateAndReturnHourFreqForUser(eventLog)
	hourScore = calculateSubscore(hourFreq)*Weight.HOURS
	return hourScore

def calculateDaysScore(eventLog):
	dayFreq = updateService.updateAndReturnDayFreqForUser(eventLog)
	dayScore = calculateSubscore(dayFreq)*Weight.DAYS
	return dayScore

def calculateServerScore(eventLog):
	serverFreq = updateService.updateAndReturnServerFreqForUser(eventLog)
	serverScore = calculateSubscore(serverFreq) * Weight.SERVER
	return serverScore

def calculateIpScore(eventLog):
	ipFreq = updateService.updateAndReturnIpFreqForUser(eventLog)
	ipScore = calculateSubscore(ipFreq) * Weight.IP
	return ipScore

def calculateSubscore(freq):
	subscore = math.log(freq, 2)
	subscore = subscore*-10
	if(subscore>100):
		return 100
	return subscore

def calculateSuccessScore(success):
	successScore = Weight.SUCCESS
	if success:
		successScore = 0
	return successScore

def calculateIpLocationScore(ipAddress):
	ipScore = Weight.EXT
	if IpAddress.checkIpForVpn(ipAddress):
		ipScore=Weight.VPN
	if IpAddress.checkIpForInternal(ipAddress):
		ipScore=Weight.INT
	return ipScore
