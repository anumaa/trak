#!/usr/bin/python


from tkinter import *
from tkinter import ttk
import pickle
import atexit
import os.path
from datetime import date, timedelta

from project import * 
from task import * 


class Trak(Frame):


	def __init__(self, parent, tasks):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.tasks = tasks
		self.initUI()
		self.previousTask = -1
		self.editListVisible = FALSE
		self.visuVisible = FALSE


	def onExit(self):
		print('onExit')
		#pickle
		self.destroy()


	def start1(self, event):
		self.start()


	def start(self):

		print("self.start, current: " + str(self.taskList.current()))
		whichTask = int(self.taskList.current())

		print(self.tasks[whichTask].getName())
		print(whichTask)
		t = self.tasks[whichTask]

		#print "previous: " + str(self.previousTask)
		if(self.previousTask != -1): 
			self.stop()
		#whichTask = self.newTask.get()
		#print "which: " + str(whichTask)
		
		task = self.tasks[whichTask]
		taskTime = str(task.getTotalTime()) 
		
		print ('START ' + str(task.__str__('red')) + "SESSION " + str(len(self.tasks[whichTask].getSessions())+1) + " " + taskTime)  
		self.tasks[whichTask].startSession()
		self.previousTask = whichTask

		self.stopButton.config(relief=RAISED)
		self.startButton.config(relief=SUNKEN)

	
	def stop(self):
		print('self.stop()')
		self.tasks[self.previousTask].endSession()
		self.stopButton.config(relief=SUNKEN)
		self.startButton.config(relief=RAISED)
		print ('STOP  ' + str(self.tasks[self.previousTask].strLatestSession()))
		
		
	def export(self):


		today = datetime.datetime.today().date()

		filename = 'trak-'+str(today)+'.csv'
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


	def editList(self):

		if self.editListVisible == FALSE:
			self.taskListButton = Button(self, command = self.updateList, text='Update')
			self.taskListButton.grid(row=2, column=0, columnspan=4)
			self.taskListText = Text(self, height=10, width=30)
			for t in self.tasks:
				self.taskListText.insert(END, t.getName()+'\n')
			self.taskListText.grid(row=1, column=0, columnspan=4)
			self.editListVisible = TRUE
			self.editButton.config(relief=SUNKEN)
		else:
			self.taskListButton.grid_remove()
			self.taskListText.grid_remove()
			self.editListVisible = FALSE
			self.startButton.grid()
			self.editButton.config(relief=RAISED)


	##
	##	Summarize the current week
	##
	def visualize(self):

		x0 = 0
		y0 = 10
		h = 30
		w = 0
		maxWidth = self.winfo_width()
		maxHeight = len(self.tasks)*(h+30)

		weekday = datetime.datetime.today().weekday()
		#print("today: " + str(weekday))
		#timestamp of Monday 00:00?
		timenow = datetime.datetime.time(datetime.datetime.now())
		weekstart = datetime.datetime.today()-timedelta(days=weekday)-timedelta(hours=timenow.hour, minutes=timenow.minute, microseconds=timenow.microsecond, seconds=timenow.second)



		if not self.visuVisible:

			self.visuVisible = TRUE
			self.vis = Canvas(self, width=maxWidth, height=maxHeight)
			self.vis.grid(row=2,column=0,columnspan=5)
			self.vis.grid(row=2,column=0,columnspan=5)

			self.exportButton = Button(self, command = self.export, text='Export')
			self.exportButton.grid(row=3, column = 0, columnspan = 5)

			allTotal = 0
			for t in self.tasks:
				for s in t.getSessions():
					if s.getStartTime() > weekstart.timestamp():
						allTotal = allTotal + t.getTotalTime()


			self.vis.create_text(x0+30, y0+10, text='THIS WEEK')
			y0 = y0 + 30
			for t in self.tasks:

				taskTotal = t.getTotalTime()
				taskHMS = time.strftime('%H:%M:%S', time.gmtime(taskTotal))
				taskText = t.name + ': ' + str(taskHMS)
				self.vis.create_text(maxWidth-len(t.name)*10, y0+15, text=taskText )

				for s in t.getSessions():
					if s.getStartTime() > weekstart.timestamp():
						if(taskTotal != 0):
							w = (s.getTotalTime()*1.0 / allTotal)*maxWidth

							#print("\ns.tot: " + str(tot))
							#print("w: " + str(w))
							#print("alltot: " + str(allTotal))
							self.vis.create_rectangle(x0, y0, x0+w, y0+h, fill="green")
							x0 = x0+w

				x0 = 0
				y0 = y0 + h + 10

			self.outputButton.config(relief=SUNKEN)
		else:
			self.visuVisible = FALSE
			self.vis.grid_remove()
			self.exportButton.grid_remove()
			self.outputButton.config(relief=RAISED)


	def updateList(self):
		print('updated list')

		allTasks = self.taskListText.get("1.0",END)
		updatedTasks = allTasks.split('\n')

		taskNames = []
		for t in self.tasks:
			taskNames.append(t.getName())

		for t in self.tasks:
			if t.getName() not in updatedTasks:
				t.setStatus('archived')

		for ut in updatedTasks:
			if ut not in taskNames and ut != '':
				print(ut)
				newTask = Task(ut)
				self.tasks.append(newTask)

		names = (o.name for o in self.tasks)
		print(self.tasks)
		self.updateTaskList()



	def updateTaskList(self):
		tnames = []
		for t in self.tasks:
			tnames.append(t.getName())
		self.taskList['values'] = tnames



	def initUI(self):

		self.parent.title("trak v0.1")

		self.pack(fill=BOTH, expand=False)
		self.var = BooleanVar()

		taskNames = []
		for t in self.tasks:
			taskNames.append(t.getName())

		self.newTask = StringVar()
		self.taskList = ttk.Combobox(self, textvariable=self.newTask, values=taskNames)

		self.taskList.bind('<<ComboboxSelected>>',self.start1)

		if len(self.tasks) > 0:
			self.taskList.current(0)
		self.taskList.grid(row=0,column=0)

		self.playImg = PhotoImage(file='images/play.png')
		self.startButton = Button(self, justify = LEFT, command = self.start, image=self.playImg)
		self.startButton.grid(row=0,column=1)

		self.pauseImg = PhotoImage(file='images/pause.png')
		self.stopButton = Button(self, justify = LEFT, command = self.stop, image=self.pauseImg)
		self.stopButton.grid(row=0,column=2)

		self.ejectImg = PhotoImage(file='images/eject.png')
		self.editButton = Button(self, justify = LEFT, command=self.editList, image=self.ejectImg)
		self.editButton.grid(row=0,column=3)

		self.outputImg = PhotoImage(file='images/menu-lines.png')
		self.outputButton = Button(self, justify = LEFT, command=self.visualize, image=self.outputImg)
		self.outputButton.grid(row=0,column=4)


def doSomethingOnExit(tasks):
	print ("atexit" + str(len(tasks)))
	pickle.dump( tasks, open( "trak.p", "wb" ) )


def main():

	#tasks = []
	#for i in range(0,5):
	#	tname = 'task'+str(i)
	#	t = Task(tname)
	#	tasks.append(t)


	root = Tk()

	if os.path.exists('trak.p'):
		tasks = pickle.load( open( "trak.p", "rb" ) )
		app = Trak(root, tasks)

	else:

		tasks = []

		app = Trak(root, tasks)
		app.editList()


	atexit.register(doSomethingOnExit, tasks)
	root.wm_attributes("-topmost", 1)
	root.mainloop()


if __name__ == '__main__':
	main()  
