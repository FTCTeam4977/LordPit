class FTCBowledOverStringConversions:

	@staticmethod	
	def AutonomousBall(input):
		if input == 1:
			return "Front"
		if input == 2:
			return "Back"
		return "None"

	@staticmethod	
	def AutonomousPark(input):
		if input == 1:
			return "Back"
		if input == 2:
			return "Front"
		return "None"

	@staticmethod	
	def AutonomousBlock(input):
		if input:
			return "Yes"
		else:
			return "No"

	@staticmethod	
	def TeleCrateActions(input):
		if input == 2:
			return "Lift+Fill"
		if input == 1:
			return "Fill"
		return "Nothing"

	@staticmethod	
	def TeleBowlingBall(input):
		if input == 2:
			return "In hole"
		if input == 1:
			return "On ramp"
		return "None"


class FTCBowledOverPointConversions:
	@staticmethod
	def AutonomousBall(input):
		if input == 1:
			return 10
		if input == 2:
			return 20
		return 0
	
	@staticmethod
	def AutonomousPark(input):
		if input == 1:
			return 5
		if input == 2:
			return 10
		return 0
	
	@staticmethod
	def TeleMaxCrateLevel(input):
		return input*10;
	
	@staticmethod
	def TeleBallsPerCrate(input):
		return input*2
	
	@staticmethod
	def TeleMagBallsScored(input):
		return input*25
	
	@staticmethod
	def TeleBall(input):
		if input == 1:
			return 20
		if input == 2:
			return 30
		return 0