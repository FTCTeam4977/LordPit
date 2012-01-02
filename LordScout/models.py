from django.db import models
 
class ScoutingReport(models.Model):
	uuid = models.CharField(max_length=58)
	team = models.IntegerField()
	
	# Autonomous
	autoBowlingBall = models.IntegerField()
	autoParking = models.IntegerField()
	autoBlocking = models.IntegerField()
	
	# Teleop
	teleCrateActions = models.IntegerField()
	teleMaxCrateLevel = models.IntegerField()
	teleNumOfCrates = models.IntegerField()
	teleNumOfStacks = models.IntegerField()
	teleBallsPerCrate = models.IntegerField()
	teleMagBallsScored = models.IntegerField()
	teleBowlingBall = models.IntegerField()
	
	extraNotes = models.CharField(max_length=500)
	
