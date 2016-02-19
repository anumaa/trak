#!/usr/bin/python

from tkinter import *
from tkinter import ttk
import pickle
import atexit
import os.path
from datetime import date, timedelta

from project import * 
from task import * 

DATASTORAGE = 'trak.p'

class Trak(Frame):


	def __init__(self, parent, project):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.project = project
		self.initUI()
		self.previousTask = -1
		self.editListVisible = FALSE
		self.visuVisible = FALSE


	def initUI(self):

		self.parent.title("trak v0.1")
		self.pack(fill=BOTH, expand=False)

		taskNames = self.project.getActiveTaskNames()

		self.newTask = StringVar()
		self.taskList = ttk.Combobox(self, textvariable=self.newTask, values=taskNames)
		self.taskList.bind('<<ComboboxSelected>>',self.start1)

		if len(self.project.getActiveTasks()) > 0:
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



	"""Needed detour by the project list combobox

	"""
	def start1(self, event):
		self.start()


	"""Starts a new session of the currently selected task

	"""
	def start(self):
		#self.project.startTask(self.taskList.current())
		self.project.startTask(self.taskList.get())
		self.stopButton.config(relief=RAISED)
		self.startButton.config(relief=SUNKEN)


	"""Stops the currently ongoing session of the ongoing task

	"""
	def stop(self):
		self.project.stopTask()
		self.stopButton.config(relief=SUNKEN)
		self.startButton.config(relief=RAISED)


	"""Exporting the summary per task for the ongoing week (currently)

	TODO: modifying according to new specs
	"""
	def export(self):
		self.project.export('\t')


	"""Editing the list of active tasks

	If a task is erased from this view, its status is set to 'archived',
	but it's not deleted from long-term storage

	TODO:  user interface for unarchiving tasks?
	"""
	def editList(self):

		#if not visible, show
		if self.editListVisible == FALSE:
			self.taskListText = Text(self, height=10, width=30)

			for taskName in self.project.getActiveTaskNames():  #todo: unsplit?
				self.taskListText.insert(END, taskName+'\n')
			self.taskListText.grid(row=1, column=0, columnspan=4)

			self.editListVisible = TRUE
			self.editButton.config(relief=SUNKEN)
		#if visible & button was pushed, hide
		else:
			self.updateList()
			#self.taskListButton.grid_remove()
			self.taskListText.grid_remove()
			self.editListVisible = FALSE
			self.startButton.grid()
			self.editButton.config(relief=RAISED)



	"""Updates the tasks

	-genuinely new tasks are added
	-reoccurring, archived tasks are reactivated
	-tasks deleted from the on-screen list, which appear on the project tasks, are archived
	"""
	def updateList(self):

		allTasks = self.taskListText.get("1.0",END)
		self.project.updateTasks(allTasks)
		self.taskList['values'] = self.project.getActiveTaskNames()
		self.taskList.current(len(self.taskList['values'])-1)  #the last one is active
		self.start()


	"""Visual summary the current week (rough draft)

	TODO: redefine specifications, better encapsulation ?
	"""
	def visualizeWeek(self):

		x0 = 0
		y0 = 10
		h = 30
		w = 0
		maxWidth = self.winfo_width()
		maxHeight = len(self.project.getActiveTasks())*(h+30)

		weekday = datetime.datetime.today().weekday()
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

			self.vis.create_text(maxWidth/2, y0+10, text='THIS WEEK')
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


"""Saves the updated project state before closing the application window

"""
def handleExit(project):
	pickle.dump( project, open( DATASTORAGE, "wb" ) )


def main():

	root = Tk()

	if os.path.exists(DATASTORAGE):
		project = pickle.load( open( DATASTORAGE, "rb" ) )
		app = Trak(root, project)

	else:
		project = Project()
		app = Trak(root, project)

	if len(project.getActiveTasks()) == 0:
		app.editList()


	atexit.register(handleExit, project)
	root.wm_attributes("-topmost", 1)
	root.mainloop()


if __name__ == '__main__':
	main()  
