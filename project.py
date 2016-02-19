#!/usr/bin/python
#import task2
from task import *
from datetime import date, timedelta

class Project: 

	def __init__(self): 
		self.name = ''
		self.tasks = []
		self.previousTask = -1

	#def __init__(self, tasks):
	#	self.tasks = tasks
	#	self.previousTask = -1

	def initTasks(self, tasks):
		self.tasks = tasks


	def addTasks(self, taskString):
		newTasks = taskString.split('\n')

		for newTaskName in newTasks:
			if newTaskName != '':
				newTask = Task(newTaskName)
				self.tasks.append(newTask)


	def getTasks(self): 
		return self.tasks


	def getTaskNames(self):

		if len(self.tasks) > 0:
			names = []
			for t in self.tasks:
				names.append(t.name)
			return names
		else:
			return ''


	def getTask(self, num):
		return self.tasks[num]


	def addTask(self, taskName):
		newTask = Task(taskName)
		self.tasks.append(newTask)


	def startTask(self, taskNumber):
		#print "previous: " + str(self.previousTask)
		if(self.previousTask != -1):
			self.stopTask()
		#whichTask = self.newTask.get()
		#print "which: " + str(whichTask)

		task = self.tasks[taskNumber]
		taskTime = str(task.getTotalTime())

		#print ('START ' + str(task.__str__('red')) + "SESSION " + str(len(self.tasks[whichTask].getSessions())+1) + " " + taskTime)
		self.tasks[taskNumber].startSession()
		self.previousTask = taskNumber


	def getTimeThisWeek(self):
		weekday = datetime.datetime.today().weekday()
		#print("today: " + str(weekday))
		#timestamp of Monday 00:00?
		timenow = datetime.datetime.time(datetime.datetime.now())
		weekstart = datetime.datetime.today()-timedelta(days=weekday)-timedelta(hours=timenow.hour, minutes=timenow.minute, microseconds=timenow.microsecond, seconds=timenow.second)

		totalSec = 0
		for t in self.tasks:
			for s in t.getSessions():
				if s.getStartTime() > weekstart.timestamp():
					totalSec = totalSec + t.getTotalTime()

		return totalSec



	def stopTask(self):
		print('self.stop()')
		self.tasks[self.previousTask].endSession()
		print ('STOP  ' + str(self.tasks[self.previousTask].strLatestSession()))


	def export(self):
		today = datetime.datetime.today().date()

		filename = 'data/trak-'+str(today)+'.csv'
		print(filename)
		exportFile = open(filename, 'w')


		exportFile.write('TASK\tHOURS\tMINUTES\tSECONDS\n')
		for t in self.tasks:

			taskTotal = t.getTotalTime()
			taskHMS = time.strftime('\t%H\t%M\t%S\n', time.gmtime(taskTotal))

			line = t.name + taskHMS
			exportFile.write(line)
			print (t.getName() + " TOTAL: " + str(t.getTotalTime()))
			i = 1
			for s in t.getSessions():
				print ("\tSESSION " + str(i) + ": " + str(s.getTotalTime()))
				line = "\tSESSION " + str(i) + ": " + str(s.getTotalTime())
				#print time.strftime('%H:%M:%S', time.localtime(s.getTotalTime()))
				i = i + 1
				#exportFile.write(line)
		
	def __str__(self):
		s = ''
		for t in self.tasks: 
			s = s + t.name + ': ' + str(t.totalTime) + '\n'
		return s


#p = Project('Testiprojekti 1')

#for i in range(1,5):
#	t = Task('task ' + str(i))
#	p.addTask(t)
	
#print(p)
	
