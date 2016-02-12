#!/usr/bin/python
#import task2
from task import *

class Project: 
	'one task'
	
	name = '' 
	
	
	def __init__(self): 
		self.name = ''
		self.tasks = []

	def __init__(self, name): 
		self.name = name
		self.tasks = []		

	def getTasks(self): 
		return self.tasks
	
	def addTask(self, task): 
		self.tasks.append(t)
		
	def __str__(self):
		s = ''
		for t in self.tasks: 
			s = s + t.name + ': ' + str(t.totalTime) + '\n'
		return s


p = Project('Testiprojekti 1')

for i in range(1,5): 
	t = Task('task ' + str(i))
	p.addTask(t)
	
print(p)
	
