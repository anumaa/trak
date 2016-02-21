#!/usr/bin/python

from tkinter import *
from tkinter import ttk
import pickle
import atexit
import os.path
from datetime import date, timedelta

from project import * 
#from task import * 

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


	"""Constructor. Initalizes the main widgets 
	
	Icons made by Robin Kylander: http://www.flaticon.com/authors/robin-kylander
	License: CC 3.0 BY
	"""
	def initUI(self):

		self.parent.title("trak v0.1")
		self.pack(fill=BOTH, expand=False)

		taskNames = self.project.getActiveTaskNames()

		self.newTask = StringVar()
		#rather a regular option menu 
		self.taskList = ttk.Combobox(self, textvariable=self.newTask, font=("Helvetica",12), values=taskNames, background='white')
		self.taskList.bind('<<ComboboxSelected>>',self.start1)

		if len(self.project.getActiveTasks()) > 0:
			self.taskList.current(0)
		self.taskList.grid(row=0,column=0)

		self.playImg = PhotoImage(file='images/play.png')
		self.startButton = Button(self, justify = LEFT, command = self.start, image=self.playImg, background='white')
		self.startButton.grid(row=0,column=1)

		self.pauseImg = PhotoImage(file='images/pause.png')
		self.stopButton = Button(self, justify = LEFT, command = self.stop, image=self.pauseImg,  background='white')
		self.stopButton.grid(row=0,column=2)

		self.addImg = PhotoImage(file='images/add.png')
		self.addButton = Button(self, justify = LEFT, command=self.editList, image=self.addImg, background='white')
		self.addButton.grid(row=0,column=3)

		self.outputImg = PhotoImage(file='images/list.png')
		self.outputButton = Button(self, justify = LEFT, command=self.visualize, image=self.outputImg, background='white')
		self.outputButton.grid(row=0,column=4)


	"""Editing the list of active tasks

	If a task is erased from this view, its status is set to 'archived',
	but it's not deleted from long-term storage

	If a task is added that has a name of a task that has been archived, 
	the task status is set back to active 
	"""
	def editList(self):

		taskListLabelText = 'Add or remove tasks\n(deleted tasks will be archived)'
		#if not visible, show
		if self.editListVisible == FALSE:
			
			self.taskListLabel = Label(self, text=taskListLabelText, font='Helvetica, 12')
			self.taskListLabel.grid(row=1, column=0, columnspan=5)
			
			self.taskListText = Text(self, height=10, width=25, background='white')

			for taskName in self.project.getActiveTaskNames():  #todo: unsplit?
				self.taskListText.insert(END, taskName+'\n')
			self.taskListText.grid(row=2, column=0, columnspan=5, sticky='NSWE')

			self.editListVisible = TRUE
			self.addButton.config(relief=SUNKEN, background='lightgrey')
		#if visible & button was pushed, hide
		else:
			self.updateList()
			self.taskListLabel.grid_remove()
			self.taskListText.grid_remove()
			self.editListVisible = FALSE
			self.startButton.grid()
			self.addButton.config(relief=RAISED, background='white')


	"""Updates the tasks

	-genuinely new tasks are added
	-reoccurring, archived tasks are reactivated
	-tasks deleted from the on-screen list, which appear on the project tasks, are archived
	"""
	def updateList(self):

		allTasks = self.taskListText.get("1.0",END)
		if len(allTasks) > 0:
			self.project.updateTasks(allTasks)
			self.taskList['values'] = self.project.getActiveTaskNames()
			if len(self.taskList['values']) > 0: 
				self.taskList.current(len(self.taskList['values'])-1)  #the last one is active
				self.start()
			


	"""Visual summary the current week (rough draft)

	TODO: re-spec according to user needs, refactor into clearer modules
	"""
	def visualize(self):

		x0 = 10
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
			self.vis = Canvas(self, width=maxWidth-2, height=maxHeight, background='white')
			self.vis.grid(row=3,column=0,columnspan=5)
			self.vis.grid(row=3,column=0,columnspan=5)

			self.exportButton = Button(self, command = self.export, text='Export')
			self.exportButton.grid(row=4, column = 0, columnspan = 5)

			allTotal = 0
			allTotal = self.project.getTimeThisWeek()

			self.vis.create_text(maxWidth/2, y0+10, text='THIS WEEK', font=('Helvetica-Bold', 12))
			y0 = y0 + 30
			for t in self.project.getActiveTasks(): #self.project.tasks:

				
				taskTotal = t.getTotalTime()

				for s in t.sessions:
					if s.startTime > weekstart.timestamp():
						if(taskTotal != 0):
							w = (s.getTotalTime()*1.0 / allTotal)*maxWidth
							self.vis.create_rectangle( x0, y0, x0+w, y0+h,fill="green")
							x0 = x0+w
							
				taskHMS = time.strftime('%H:%M:%S', time.gmtime(taskTotal))
				taskText = t.name + ': ' + str(taskHMS)
				self.vis.create_text(maxWidth/7*4, y0+10, anchor='nw', text=taskText )

				x0 = 10
				y0 = y0 + h + 10

			self.outputButton.config(relief=SUNKEN, background='lightgrey')
		else:
			self.visuVisible = FALSE
			self.vis.grid_remove()
			self.exportButton.grid_remove()
			self.outputButton.config(relief=RAISED, background='white')
		

	"""Needed detour by the project list combobox

	"""
	def start1(self, event):
		self.start()


	"""Starts a new session of the currently selected task

	"""
	def start(self):
		self.project.startTask(self.taskList.get())
		self.stopButton.config(relief=RAISED, background='white')
		self.startButton.config(relief=SUNKEN, background='lightgrey')


	"""Stops the currently ongoing session of the ongoing task

	"""
	def stop(self):
		self.project.stopTask()
		self.stopButton.config(relief=SUNKEN, background='lightgrey')
		self.startButton.config(relief=RAISED, background='white')


	"""Exporting the summary per task for the ongoing week (currently)

	TODO: modifying according to new specs
	"""
	def export(self):
		self.project.export('\t')


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
	root.configure(background='white')
	root.mainloop()


if __name__ == '__main__':
	main()  
