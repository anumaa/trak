#!/usr/bin/python

from session import *

class Task: 
	'one task'
	
	name = '' 


	def __init__(self, name):
		self.name = name
		self.sessions = []
		self.totalTime = 0
		self.status = 'active'
		

	def startSession(self):
		
		s = Session()
		self.sessions.append(s)


	def endSession(self): 
		#end the last session of the list 
		#update cumulative total time 
		
		latestSession = self.sessions[len(self.sessions)-1]
		latestSession.endSession()
		
		st = latestSession.getStartTime()
		en = latestSession.getEndTime()
		tot = latestSession.getTotalTime() 

		self.totalTime = self.totalTime + latestSession.getTotalTime()


	"""

	"""
	def isActive(self):
		if self.status == 'active':
			return True
		return False


	def archive(self):
		self.status = 'archived'


	def activate(self):
		self.status = 'active'


	def getTotalTime(self):
		return self.totalTime


	def getSessions(self):
		return self.sessions
		
		
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
