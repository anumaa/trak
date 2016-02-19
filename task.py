#!/usr/bin/python

from session import *

class Task: 
	'one task'
	
	name = '' 
	
	def __init__(self): 
		self.name = ''
		self.sessions = []
		self.totalTime = 0
		self.status = 'uninitialized'
		

	def __init__(self, name): 
		self.name = name
		self.sessions = []
		self.totalTime = 0
		self.status = 'active'
		

	def startSession(self): 
		
		s = Session()
		self.sessions.append(s)
		#print "task2.startSession: starting session " + str(len(self.sessions))
		
		
		
	def endSession(self): 
		#end the last session of the list 
		#update cumulative total time 
		
		latestSession = self.sessions[len(self.sessions)-1]
		latestSession.endSession()
		
		st = latestSession.getStartTime()
		en = latestSession.getEndTime()
		tot = latestSession.getTotalTime() 
		
		#print "task2.endSession: ending session " + str(len(self.sessions)) + ", session: " + str(tot) + " task: " + str(self.totalTime) # + "\t" + str(en) + "\t" + str(tot) 
		
		
		#print latestSession
		
		self.totalTime = self.totalTime + latestSession.getTotalTime()
		
		
		
	def getName(self): 
		return self.name
		

	def getStatus(self):
		return self.status


	def setStatus(self, newStatus):
		self.status = newStatus


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
		
		#print "SESSIONS: " + str(len(self.sessions))
		
		r = r + 'SESSION ' + str(len(self.sessions)) #+ " " + str(self.sessions[len(self.sessions)-1])

		return r


#task1 = Task2('eka')
#task1.startSession()
#time.sleep(1)
#task1.endSession()

#task1.startSession()
#time.sleep(2)
#task1.endSession()

#task1.startSession()
#time.sleep(3)
#task1.endSession()

#print(task1)
