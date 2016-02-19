#!/usr/bin/python
from task import *
from datetime import date, timedelta


class Project: 

	def __init__(self): 
		self.name = ''
		self.tasks = []
		self.previousTask = None


	def initTasks(self, tasks):
		self.tasks = tasks


	#
	#	Adds tasks from \n -separated string
	#	-If task doesn't already exist in the current list, it's added (addTask -method checks for existence)
	#	-If a currently active task is deleted from the visible list, its status is set to 'archived' (TODO)
	#	(it will not appear in the list of active tasks, but will appear on the time reports (marked archived)
	#	-if an archived taskname is reused, the task's status is set to active again (possibly confusing, needs discussion)
	#
	def updateTasks(self, taskString):
		newTasks = taskString.split('\n')

		for newTaskName in newTasks:
			self.addTask(newTaskName)

		# task was deleted from list -> archive!
		#if taskName != '' and
		for existingTask in self.tasks:
			if existingTask.isActive() and existingTask.name not in newTasks:
				existingTask.archive()
				print('archived: ' + existingTask.name)



	def getActiveTasks(self):
		rt = []
		for t in self.tasks:
			if t.isActive():
				rt.append(t)
		return rt


	def getArchivedTasks(self):
		rt = []
		for t in self.tasks:
			if t.isArchived():
				rt.append(t)
		return rt


	#
	#	Returns a list of task names (strings)
	#
	def getTaskNames(self):

		if len(self.tasks) > 0:
			names = []
			for t in self.tasks:
				names.append(t.name)
			return names
		else:
			return ''


	def getActiveTaskNames(self):
		if len(self.tasks) > 0:
			names = []
			for t in self.tasks:
				if t.isActive():
					names.append(t.name)
			return names
		else:
			return ''


	#
	#	Get task by index
	#	TODO: verify correct behaviour with nonactive tasks
	#
	def getTask(self, num):
		return self.tasks[num]




	#
	#	Find a task by its unique name (case-sensitive)
	#
	def getTaskByName(self, taskName):
		for t in self.tasks:
			if t.name == taskName:
				return t
		return None


	#
	#	Get currently active tasks
	#
	def getActiveTasks(self):
		at = []
		for t in self.tasks:
			if t.isActive():
				at.append(t)
		return at


	#
	#	Add new task
	#	Check for empty name given, and existence of the task in the currently active tasks
	#
	def addTask(self, taskName):

		t = self.getTaskByName(taskName)

		# genuinely new task
		if taskName != '' and t == None: #taskName not in self.getTaskNames():
			newTask = Task(taskName)
			self.tasks.append(newTask)

		# same task name as previously active task -> activate!
		if taskName != '' and t != None:
			t.activate()
			print('reactivating! '+ taskName)


	#
	#
	#
	def startTask(self, taskName):
		#print "previous: " + str(self.previousTask)
		if(self.previousTask != None):
			self.stopTask()
		#whichTask = self.newTask.get()
		#print "which: " + str(whichTask)

		task = self.getTaskByName(taskName)#self.tasks[taskNumber]
		taskTime = str(task.getTotalTime())

		#print ('START ' + str(task.__str__('red')) + "SESSION " + str(len(self.tasks[whichTask].getSessions())+1) + " " + taskTime)
		print ('START  ' + str(task.strLatestSession()))
		task.startSession()
		self.previousTask = task


	#
	#
	#
	def getTimeThisWeek(self):
		weekday = datetime.datetime.today().weekday()
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
		self.previousTask.endSession()
		print ('STOP  ' + str(self.previousTask.strLatestSession()))


	def export(self, separator):
		today = datetime.datetime.today().date()

		filename = 'data/trak-'+str(today)+'.csv'
		print(filename)
		exportFile = open(filename, 'w')

		exportFile.write('TASK'+separator+'HOURS'+separator+'MINUTES'+separator+'SECONDS\n')
		for t in self.tasks:

			taskTotal = t.getTotalTime()
			taskHMS = time.strftime(separator+'%H'+separator+'%M'+separator+'%S\n', time.gmtime(taskTotal))

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
	
