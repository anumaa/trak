#!/usr/bin/python

import datetime
import time 

class Session:
	totalTime = 0
	
	def __init__(self): 
		self.totalTime = 0 # datetime.datetime.now().time() 
		self.startTime = int(time.time())  #get time NOW (seconds format?) 
		self.endTime = 0
		
	def __print__(self): 
		return str(self.startTime)
		
	def endSession(self): 
		self.endTime = int(time.time())
		self.totalTime = self.endTime-self.startTime
		
	def getTotalTime(self):
		return self.totalTime
