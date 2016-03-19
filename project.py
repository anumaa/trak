#!/usr/bin/python
from task import *
from datetime import date, timedelta
import dateutil

"""Project contains the current set of tasks (both active and archived)

Currently the application only contains one project (could be taken 
as a single client). Future versions will probably enable tracking 
multiple projects simultaneously (tasks done for several clients) 
"""
class Project: 

	def __init__(self): 
		self.name = ''
		self.tasks = []
		self.previousTask = None


	def initTasks(self, tasks):
		self.tasks = tasks


	"""Adds tasks from \n -separated string

		-If task doesn't already exist in the current list, it's added (addTask -method checks for existence)
		-If a currently active task is deleted from the visible list, its status is set to 'archived' (TODO)
		(it will not appear in the list of active tasks, but will appear on the time reports (marked archived)
		-if an archived taskname is reused, the task's status is set to active again (possibly confusing, needs discussion)
	"""
	def updateTasks(self, taskString):
		newTasks = taskString.split('\n')

		for newTaskName in newTasks:
			self.addTask(newTaskName)

		for existingTask in self.tasks:
			if existingTask.isActive() and existingTask.name not in newTasks:
				existingTask.archive()
				#print('archived: ' + existingTask.name)


	"""Returns a list of active tasks

	"""
	def getActiveTasks(self):
		rt = []
		for t in self.tasks:
			if t.isActive():
				rt.append(t)
		return rt


	"""Returns a list of archived tasks 

	"""
	def getArchivedTasks(self):
		rt = []
		for t in self.tasks:
			if t.isArchived():
				rt.append(t)
		return rt


	"""Returns a list of task names (strings)

	"""
	def getTaskNames(self):

		if len(self.tasks) > 0:
			names = []
			for t in self.tasks:
				names.append(t.name)
			return names
		else:
			return ''


	"""Returns a list of active task names 

	"""
	def getActiveTaskNames(self):
		if len(self.tasks) > 0:
			names = []
			for t in self.tasks:
				if t.isActive():
					names.append(t.name)
			return names
		else:
			return ''


	"""Get task by index

	TODO: verify correct behaviour with nonactive tasks
	"""
	def getTask(self, num):
		return self.tasks[num]




	"""Find a task by its unique name (case-sensitive)

	"""
	def getTaskByName(self, taskName):
		for t in self.tasks:
			if t.name == taskName:
				return t
		return None


	"""Get currently active tasks

	"""
	def getActiveTasks(self):
		at = []
		for t in self.tasks:
			if t.isActive():
				at.append(t)
		return at


	"""Add new task
 
		Check for empty name given, and existence of the task in the currently active tasks
		Truncates the task name to max. 25 characters 
	"""
	def addTask(self, taskName):

		taskName = taskName[0:25]
		t = self.getTaskByName(taskName)

		# genuinely new task
		if taskName != '' and t == None: #taskName not in self.getTaskNames():
			newTask = Task(taskName)
			self.tasks.append(newTask)

		# same task name as previously active task -> activate!
		if taskName != '' and t != None:
			t.activate()


	"""Starts another session of the currently active task 

	"""
	def startTask(self, taskName):

		#find the task from the task list
		newTask = self.getTaskByName(taskName)
		#check it's not null

		#no previous task
		if self.previousTask == None or self.previousTask == newTask:

			#start a new session, end the latest one first
			newTask.endSession()
			newTask.startSession()

		#otherwise need to manage ending of the different previous task
		else:
			self.previousTask.endSession()
			newTask.startSession()

		self.previousTask = newTask



	"""Stops the current session of the currently active task 

	"""
	def stopTask(self):

		#explicit pause
		if self.previousTask != None:
			self.previousTask.endSession()


	"""Cumulative time per task over the current week (starting Monday midnight) 

	"""
	def getTimeThisWeek(self):
		weekday = datetime.datetime.today().weekday()
		timenow = datetime.datetime.time(datetime.datetime.now())
		weekstart = datetime.datetime.today()-timedelta(days=weekday)-timedelta(hours=timenow.hour, minutes=timenow.minute, microseconds=timenow.microsecond, seconds=timenow.second)

		totalSec = 0
		for t in self.tasks:
			for s in t.sessions:
				if s.startTime > weekstart.timestamp():
					totalSec = totalSec + t.getTotalTime()

		return totalSec



	"""Exports the (active) tasks as a comma-separated file (rough draft) 
	
	TODO: specify output format according to user needs 
	"""
	def export(self, separator):
		today = datetime.datetime.today().date()

		filename = 'trak-'+str(today)+'.csv'
		#print(filename)
		exportFile = open(filename, 'w')

		exportFile.write('TASK'+separator+'HOURS'+separator+'MINUTES'+separator+'SECONDS\n')
		for t in self.tasks:

			taskTotal = t.getTotalTime()
			taskHMS = time.strftime(separator+'%H'+separator+'%M'+separator+'%S\n', time.gmtime(taskTotal))

			line = t.name + taskHMS
			exportFile.write(line)
			#print (t.name + " TOTAL: " + str(t.getTotalTime()))
			i = 1
			for s in t.sessions:
				#print ("\tSESSION " + str(i) + ": " + str(s.getTotalTime()))
				line = "\tSESSION " + str(i) + ": " + str(s.getTotalTime())
				i = i + 1


	def exportMonth(self, separator):
		today = datetime.datetime.today().date()






	def __str__(self):
		s = ''
		for t in self.tasks: 
			s = s + t.name + ': ' + str(t.totalTime) + '\n'
		return s

