from discovery_bot import pins
from discovery_bot import Movement
from discovery_bot import Ultrasound
from Sensor import *
from servo import Servo
import time
import datetime


class Move:
	TOO_CLOSE  = "Too Close";

	def __init__(self, start = (0,0),leftSpeed = 100, rightSpeed = 50):
		
		self.location = start
		self.x = start[0]
		self.y = start[1]

		self.leftSpeed = leftSpeed
		self.rightSpeed = rightSpeed

		self.left = Servo(pins.SERVO_LEFT_MOTOR)
		self.right = Servo(pins.SERVO_RIGHT_MOTOR)
		self.sensor = Sensor()

		self.us = Ultrasound()
		self.movement = Movement()

		self.timeSpin = 0


		print "Left Speed: ", self.leftSpeed, "\nRight Speed: ", self.rightSpeed

	def checkBoundary(self,cmSent):
		# situation 1
		# we send something and we find out that the robot is going to hit the wall if it continues, meaning the distance is greater
		#than the closest thing away, that the worst possible thing, so lets check for that first.

		#if the desired distance is greater or equal to the distance away from the closest obstacle
		cmAwayFromWall = self.sensor.getDistance()
		if (cmSent >  cmAwayFromWall):
			return "STOP"
		elif (cmSent > (cmAwayFromWall - 10)):
			return "STOP"
		elif (cmSent < (cmAwayFromWall - 10)):
			return "GOOD"

	def normalize(self, val):
		scale = 0.5 / 100
		speed = val * scale

		if val >= 0:
			speed += 0.5
		return speed

	def turn(self,angle):
		
		self.movement.setMotorSpeed(pins.SERVO_RIGHT_MOTOR, 50)
		self.movement.setMotorSpeed(pins.SERVO_LEFT_MOTOR, -100)
		time1 = 0.9

		if angle == 15:
			time1 = 0.11
		if angle == 90:
			time1 = 0.84
		else:
			a = angle % 360
			time1 = a * 0.11
		time.sleep(self.timeSpin)
		self.stop()

	def forward(self, speed = 100):
		'''
		self.left.set_normalized(1.0)
		time.sleep(0.01)
		print self.rightSpeed
		self.right.set_normalized(-self.rightSpeed)
		'''
		self.movement.setMotorSpeed(pins.SERVO_LEFT_MOTOR,100)
		time.sleep(0.01)
		self.movement.setMotorSpeed(pins.SERVO_RIGHT_MOTOR, self.rightSpeed)

	def move(self,distance):
		status = True
		result = self.checkBoundary(distance)
		cmAwayFromWall = self.sensor.getDistance()

		print cmAwayFromWall

		if (result == "STOP"):

			distanceMoved = 0
			self.movement.stop()
			return distanceMoved

		elif (result =="GOOD"):
			self.forward(100)
			time.sleep(distance/16)
		#	return status
		#account for the 5 degrees a second/ every 12 cm of curvature to the left
		distanceMoved = cmAwayFromWall - self.sensor.getDistance()
		#anglesToTurn = (distance/12) * 5
		#spinTime = anglesToTurn*0.0053763408602 # degrees per second
		# telling the robot to spin back since it turns left on its own
		#self.timedSpin(spinTime,'right')
		self.movement.stop()
		return distanceMoved

	def timedSpin(self,spinTime,direction):
			if (direction == 'left'):
				self.movement.rotate_left();
			elif (direction == 'right'):
				self.movement.rotate_right()
			time.sleep(spinTime)
			self.movement.stop()

	def turnMe(self,angle):
		
		# 90 degrees of rotation comes to approx 0.66 seconds, 2 seconds = 270* of rotation on a smooth surface
		angle = float(angle)
		
		if (angle >0):
			direction = 'right'
		else:
			direction = 'left'
		angle = abs(angle)


		if angle == 15:
			self.timeSpin = 0.0067
		elif angle == 90 or angle == -90:
			self.timeSpin = 0.0083
		else:
			self.timeSpin = 0.0067


		print self.timeSpin

		spinTime = angle * self.timeSpin # degrees per second 0.0053763408602
		self.timedSpin(spinTime,direction)

	def scanHallway(self):
		
		start = self.sensor.getDistance()
		t1 = time.time()

		self.forward()

		while True:
			try:
				r = self.sensor.getSensor('r')
				ri = int(r.strip('\r\n'))
				l = self.sensor.getSensor('l')
				le = int(l.strip('\r\n'))

				print ri,le
				raw_input("waitin ")

				if ri + le + 8 > 25:
					self.movement.stop()
					break
			except Exception as e:
				pass

		t2 = time.time()
		end = self.sensor.getDistance()

		return (start - end, t2 - t1)

	def stop(self):
		self.left.set_normalized(-1)
		self.right.set_normalized(-1)

def moveOneSecond(t = 1):

	bot = Move(leftSpeed = 100, rightSpeed = 50)
	s = ""
	
	s = raw_input("Start: ")
	start = bot.sensor.getDistance()
	bot.forward(100)
	time.sleep(t)
	bot.stop()
	end = bot.sensor.getDistance()
	print "start end ",start,end
	print start - end

def moveTest():
	while(s !='s'):
		s = raw_input("Distance: ")
		speed = raw_input("Speed (0.0 -1.0): ")

		try:
			bot.rightSpeed = float(speed)
		except:
			s = 's'

		if (s!='s'):
			print "distance away from closest: "
			print bot.move(float(s))
		
	bot.movement.stop()

def turnTest():

	count = 0
	
	
	bot.timeSpin = 0.005
	

	#full battery on Kory's Desk with paper
	#360 = ?
	#180 = 0.75
	#90 = 0.35
	#45 = 0.174
	#30 = ?
	#15 = 0.0395
	
	t = ''

	while(s !='s'):

		
		t = raw_input("Time (0.0 -1.0) or (s)top: ")
		if t == 's':
			break
		count = 0
		total = int(raw_input("Turn number: "))

		
		t = float(t)

		while count < total:
			bot.timeSpin = t
			bot.turn(s)
			count += 1
			time.sleep(1)

if __name__ == "__main__":
	
	#bot = Move()

	s = raw_input("Start: ")
	moveOneSecond()
	#print bot.scanHallway()
	