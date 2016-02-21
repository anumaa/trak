#!/usr/bin/python

import datetime
import time 

"""Task has a name and multiple working sessions 

"""
class Task: 


	def __init__(self, name):
		self.name = name
		self.sessions = []
		self.totalTime = 0
		self.status = 'active'
		
	def __str__(self): 
		r = 'TASK ' + self.name + ' ' + str(self.totalTime)
		i = 1 
		for s in self.sessions: 
			r = r + 'SESSION ' + str(i) + " " + s.__print__() 
			i = i + 1 
		return r
		

	def __str__(self, reduced): 
		r = 'TASK ' + self.name + ' ' + str(self.totalTime) + " " 
		return r
		
				
		
	def strLatestSession(self): 
		r = ''
		r = r + 'TASK ' + self.name + ' ' + str(self.totalTime) + " " 
		r = r + 'SESSION ' + str(len(self.sessions)) #+ " " + str(self.sessions[len(self.sessions)-1])
		return r
		
		
	"""Adds a new session to the task's session list 
	
	"""
	def startSession(self):
		
		s = Session()
		self.sessions.append(s)


	"""Ends the last session of the tasks session list
	
		Updates the cumulative total time count by adding the time
		of the last session 
	
	"""
	def endSession(self): 
		latestSession = self.sessions[len(self.sessions)-1]
		latestSession.endSession()
		
		#st = latestSession.startTime
		#en = latestSession.endTime
		tot = latestSession.getTotalTime() 

		self.totalTime = self.totalTime + latestSession.getTotalTime()


	"""Returns true if the task status is set to 'active'

	"""
	def isActive(self):
		if self.status == 'active':
			return True
		return False

	
	"""Sets the task status to 'archived'
	
	Could also include a timestamp for cumulative time 
	calculation purposes (TODO) 
	"""
	def archive(self):
		self.status = 'archived'


	"""Sets the task status to 'active'
	
	"""
	def activate(self):
		self.status = 'active'


	"""Returns cumulative time across all task sessions 
	
	"""
	def getTotalTime(self):
		return self.totalTime

		

"""Single unbroken session of working time 

	Session start- and endtimes are saved as timestamps 
	(resolution = seconds) 
"""
class Session:
	totalTime = 0
	
	def __init__(self): 
		self.totalTime = 0 
		self.startTime = int(time.time())
		self.endTime = 0
		
	def __print__(self): 
		return str(self.startTime)
		
	"""Ends the current session 
	
	"""
	def endSession(self): 
		self.endTime = int(time.time())
		self.totalTime = self.endTime-self.startTime
		
	def getTotalTime(self):
		return self.totalTime

