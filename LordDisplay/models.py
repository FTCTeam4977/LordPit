from django.db import models

class ConfigValue(models.Model):
	key = models.CharField(max_length=50)
	value = models.CharField(max_length=50)

class MatchResult(models.Model):
	matchNumber = models.IntegerField()
	result = models.CharField(max_length=10)