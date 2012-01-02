from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from LordScout.models import ScoutingReport

from LordScout.BowledOver import FTCBowledOverPointConversions
from LordScout.BowledOver import FTCBowledOverStringConversions

class Team:
	def __init__(self, number, reports):
		self.number = number
		self.reports = reports
		self.overall = OverallScoutingReport(reports)
	def __cmp__(self, other):
		if self.overall.avgPoints.average < other.overall.avgPoints.average:
			return -1
		if self.overall.avgPoints.average == other.overall.avgPoints.average:
			return 0	
		if self.overall.avgPoints.average > other.overall.avgPoints.average:
			return 1
				
class ScoutingItem:
	def __init__(self, raw, str, point, title):
		self.raw = raw
		self.str = str
		self.points = point
		self.title = title
	
	def GetPoints(self):
		return self.points
	
	def GetStringScore(self):
		return self.str
	
	def GetTitle(self):
		return self.title

class OverallScoutingReport:
	def __init__(self, reports):
		self.Values = []
		
		self.autoBall = ScoutingPercent("Bowling ball success rate", FTCBowledOverStringConversions.AutonomousBall)
		height = ScoutingAverage("Average highest crate")
		crates = ScoutingAverage("Average number of crates")
		stacks = ScoutingAverage("Average number of stacks")
		ballsPerCrate = ScoutingAverage("Average number of balls per crate")
		magBalls = ScoutingAverage("Average number of magnet balls scored")
		
		self.avgPoints = ScoutingAverage("Average Points")
		
		for report in reports:
			self.autoBall.add(report.autoBowlingBall.raw)
			height.add(report.teleMaxCrateLevel.raw)
			crates.add(report.teleNumOfCrates.raw)
			stacks.add(report.teleNumOfStacks.raw)
			ballsPerCrate.add(report.teleBallsPerCrate.raw)
			magBalls.add(report.teleMagBallsScored.raw)
			
			self.avgPoints.add(report.points)
			
		self.Values.append(height)
		self.Values.append(crates)
		self.Values.append(stacks)
		self.Values.append(ballsPerCrate)
		self.Values.append(magBalls)
		
		
class ScoutingAverage:
	def __init__(self, str):
		self.sum = 0
		self.totalValues = 0
		self.average = float(0)
		self.str = str
	def add(self, value):
		self.sum += value
		self.totalValues += 1
		self.average = float(self.sum)/float(self.totalValues)
	def GetAverage(self):
		return self.average

class ScoutingPercent:
	def __init__(self, str, convertCallback):
		self.spots = [0,0,0]
		self.str = str
		self.percents = [{'title':convertCallback(0),'percent':0.0},{'title':convertCallback(1), 'percent':0.0},{'title':convertCallback(2), 'percent':0.0}]
		self.total = 0
		self.convertCallback = convertCallback
	def add(self, value):
		self.spots[value] += 1
		self.total+=1
		# For loop refuses to iterate through this for some reason
		self.percents[0] = {'title':self.convertCallback(0),'percent':(float(self.spots[0])/float(self.total))*100}
		self.percents[1] = {'title':self.convertCallback(1), 'percent':(float(self.spots[1])/float(self.total))*100}
		self.percents[2] = {'title':self.convertCallback(2), 'percent':(float(self.spots[2])/float(self.total))*100}
			
		
class FormattedScoutingReport:
	def __init__(self, report):
		self.uuid = report.uuid
		self.team = report.team
		
		self.autoBowlingBall = ScoutingItem(report.autoBowlingBall, FTCBowledOverStringConversions.AutonomousBall(report.autoBowlingBall), FTCBowledOverPointConversions.AutonomousBall(report.autoBowlingBall), "Autonomous Bowling Ball")
		self.autoParking = ScoutingItem(report.autoParking, FTCBowledOverStringConversions.AutonomousPark(report.autoParking), FTCBowledOverPointConversions.AutonomousPark(report.autoParking), "Autonomous Parking")
		self.autoBlocking = ScoutingItem(report.autoBlocking, FTCBowledOverStringConversions.AutonomousBlock(report.autoBlocking), 0, "Blocks in Autonomous")
		
		self.teleCrateActions = ScoutingItem(report.teleCrateActions, FTCBowledOverStringConversions.TeleCrateActions(report.teleCrateActions), 0, "Teleop crate actions")
		self.teleMaxCrateLevel = ScoutingItem(report.teleMaxCrateLevel, report.teleMaxCrateLevel, FTCBowledOverPointConversions.TeleMaxCrateLevel(report.teleMaxCrateLevel), "Highest crate level")
		self.teleNumOfCrates = ScoutingItem(report.teleNumOfCrates, report.teleNumOfCrates, 0, "Number of crates")
		self.teleNumOfStacks = ScoutingItem(report.teleNumOfStacks, report.teleNumOfStacks, 0, "Number of stacks")
		self.teleBallsPerCrate = ScoutingItem(report.teleBallsPerCrate, report.teleBallsPerCrate, 0, "Balls per crate")
		
		self.teleMagBallsScored = ScoutingItem(report.teleMagBallsScored, report.teleMagBallsScored, FTCBowledOverPointConversions.TeleMagBallsScored(report.teleMagBallsScored), "Number of magnet balls")
		
		self.teleBowlingBall = ScoutingItem(report.teleBowlingBall, FTCBowledOverStringConversions.TeleBowlingBall(report.teleBowlingBall), FTCBowledOverPointConversions.TeleBall(report.teleBowlingBall), "End-game bowling ball placement")
		
		self.AutoScoutingItemList = [self.autoBowlingBall, self.autoParking, self.autoBlocking]
		self.TeleScoutingItemList = [self.teleCrateActions, self.teleMaxCrateLevel, self.teleNumOfCrates, self.teleNumOfStacks, self.teleBallsPerCrate, self.teleMagBallsScored, self.teleBowlingBall]
		
		self.extraNotes = report.extraNotes
		
		self.points = 0
		for item in self.AutoScoutingItemList:
			self.points += item.points
			
		for item in self.AutoScoutingItemList:
			self.points += item.points

def GetAllTeams():
	foundTeams = []
	reports = ScoutingReport.objects.all()
	for report in reports:
		teamnum = report.team
		exists = False
		for team in foundTeams:
			if ( team.number == report.team ):
				exists = True
		if exists == False:
			foundTeams.append(GetTeam(teamnum))
	return sorted(foundTeams, reverse=True)

def index(request):
	return render_to_response("LordScout/index.html", {'teams':GetAllTeams()})
	
def GetTeam(teamNumber):
	reportlist=[]
	for report in ScoutingReport.objects.all():
		if int(report.team) == int(teamNumber):
			reportlist.append(FormattedScoutingReport(report))
	return Team(teamNumber, reportlist)
	
def teamview(request, team_id):
	return render_to_response("LordScout/team.html", {'team':GetTeam(team_id)})

def importScouting(request):
	if request.method == 'POST':
		f = request.FILES['file'].read()
		lines = f.split("\n")
		for line in lines:
			data = line.split("~")
			if len(data) == 13:
				# Check if this data has already been imported
				alreadyExists = True
				try:
					ScoutingReport.objects.get(uuid=data[0])
				except Exception:
					alreadyExists = False
				
				if alreadyExists == False:
					sr = ScoutingReport(uuid=data[0],team=data[1],autoBowlingBall=data[2],autoParking=data[3],autoBlocking=data[4],teleCrateActions=data[5],teleMaxCrateLevel=data[6],teleNumOfCrates=data[7],teleNumOfStacks=data[8],teleBallsPerCrate=data[9],teleMagBallsScored=data[10],teleBowlingBall=data[11],extraNotes=data[12])
					sr.save()
	return render_to_response("LordScout/import.html", context_instance=RequestContext(request))