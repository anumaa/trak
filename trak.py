#!/usr/bin/python


from tkinter import *
from tkinter import ttk
import pickle
import atexit
import os.path
from datetime import date, timedelta

from project import * 
from task import * 

DATAPATH = 'data/trak.p'

class Trak(Frame):



	#
	#	Constructor
	#
	def __init__(self, parent, project):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.project = project
		self.initUI()
		self.previousTask = -1
		self.editListVisible = FALSE
		self.visuVisible = FALSE


	#
	#	Initializes the widgets
	#
	def initUI(self):

		self.parent.title("trak v0.1")
		self.pack(fill=BOTH, expand=False)

		taskNames = self.project.getTaskNames()

		self.newTask = StringVar()
		self.taskList = ttk.Combobox(self, textvariable=self.newTask, values=taskNames)
		self.taskList.bind('<<ComboboxSelected>>',self.start1)

		if len(self.project.tasks) > 0:
			self.taskList.current(0)
		self.taskList.grid(row=0,column=0)

		self.playImg = PhotoImage(file='images/play.png')
		self.startButton = Button(self, justify = LEFT, command = self.start, image=self.playImg)
		self.startButton.grid(row=0,column=1)

		self.pauseImg = PhotoImage(file='images/pause.png')
		self.stopButton = Button(self, justify = LEFT, command = self.stop, image=self.pauseImg)
		self.stopButton.grid(row=0,column=2)

		#TODO: respec the interface
		self.ejectImg = PhotoImage(file='images/eject.png')
		self.editButton = Button(self, justify = LEFT, command=self.editList, image=self.ejectImg)
		self.editButton.grid(row=0,column=3)

		self.outputImg = PhotoImage(file='images/menu-lines.png')
		self.outputButton = Button(self, justify = LEFT, command=self.visualizeWeek, image=self.outputImg)
		self.outputButton.grid(row=0,column=4)



	#
	#	Needed detour by the project list combobox
	#
	def start1(self, event):
		self.start()


	#
	#	Starts a new session of the currently selected task
	#
	def start(self):
		self.project.startTask(self.taskList.current())
		self.stopButton.config(relief=RAISED)
		self.startButton.config(relief=SUNKEN)


	#
	#	Stops the currently ongoing session of the ongoing task
	#
	def stop(self):
		self.project.stopTask()
		self.stopButton.config(relief=SUNKEN)
		self.startButton.config(relief=RAISED)


	#
	#	Exporting the summary per task for the ongoing week (currently)
	#	TODO: modifying according to new specs
	#
	def export(self):
		self.project.export('\t')


	#
	#	Editing the list of active tasks
	#	If a task is erased from this view, its status is set to 'archived',
	# 	but it's not deleted from long-term storage
	#
	#	TODO: specifying user interface for unarchiving tasks (if necessary)
	#
	def editList(self):

		#if not visible, show
		if self.editListVisible == FALSE:
			self.taskListButton = Button(self, command = self.updateList, text='Update')
			self.taskListButton.grid(row=2, column=0, columnspan=4)
			self.taskListText = Text(self, height=10, width=30)

			for taskName in self.project.getTaskNames():  #todo: unsplit?
				self.taskListText.insert(END, taskName+'\n')
			self.taskListText.grid(row=1, column=0, columnspan=4)

			self.editListVisible = TRUE
			self.editButton.config(relief=SUNKEN)
		#if visible & button was pushed, hide
		else:
			self.taskListButton.grid_remove()
			self.taskListText.grid_remove()
			self.editListVisible = FALSE
			self.startButton.grid()
			self.editButton.config(relief=RAISED)


	##
	##	Visual summary the current week (rough draft)
	#	TODO: redefine specifications, better encapsulation ?
	##
	def visualizeWeek(self):

		x0 = 0
		y0 = 10
		h = 30
		w = 0
		maxWidth = self.winfo_width()
		maxHeight = len(self.project.tasks)*(h+30)

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
			allTotal = self.project.getTimeThisWeek()
			#for t in self.tasks:
			#	for s in t.getSessions():
			#		if s.getStartTime() > weekstart.timestamp():
			#			allTotal = allTotal + t.getTotalTime()


			self.vis.create_text(x0+30, y0+10, text='THIS WEEK')
			y0 = y0 + 30
			for t in self.project.getActiveTasks(): #self.project.tasks:

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

		allTasks = self.taskListText.get("1.0",END)
		self.project.addTasks(allTasks)

		#taskNames = []
		#for t in self.tasks:
		#	taskNames.append(t.getName())

		#for t in self.tasks:
		#	if t.getName() not in updatedTasks:
		#		t.setStatus('archived')

		#for ut in updatedTasks:
		#	if ut not in taskNames and ut != '':
		#		print(ut)
		#		newTask = Task(ut)
		#		self.tasks.append(newTask)

		#names = (o.name for o in self.tasks)
		#print(self.tasks)

		self.taskList['values'] = self.project.getActiveTaskNames()
		print('updated list')


#
#	Saves the updated project state before closing the application window
#
def handleExit(project):
	pickle.dump( project, open( DATAPATH, "wb" ) )


def main():

	root = Tk()

	if os.path.exists(DATAPATH):
		project = pickle.load( open( DATAPATH, "rb" ) )
		app = Trak(root, project)

	else:
		project = Project()
		app = Trak(root, project)
		app.editList()


	atexit.register(handleExit, project)
	root.wm_attributes("-topmost", 1)
	root.mainloop()


if __name__ == '__main__':
	main()  
