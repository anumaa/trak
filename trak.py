#!/usr/bin/python


from tkinter import *
from tkinter import ttk
import pickle
import atexit
import os.path

from project import * 
from task import * 


class GUI(Frame):


	def __init__(self, parent, tasks):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.tasks = tasks
		self.initUI()
		self.previousTask = -1
		self.editListVisible = FALSE
		self.visuVisible = FALSE
		#self.wm_protocol("WM_DELETE_WINDOW", self.onExit)


	def loadTasks(self, tasks):
		self.tasks = tasks


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
		
		
	def printAll(self):
		for t in self.tasks: 
			print (t.getName() + " TOTAL: " + str(t.getTotalTime()))
			i = 1 
			for s in t.getSessions(): 
				print ("\tSESSION " + str(i) + ": " + str(s.getTotalTime()))
				#print time.strftime('%H:%M:%S', time.localtime(s.getTotalTime()))
				i = i + 1



	def editList(self):

		if self.editListVisible == FALSE:
			self.taskListButton = Button(self, command = self.updateList, text='Update')
			self.taskListButton.grid(row=2, column=0, columnspan=4)
			self.taskListText = Text(self, height=10, width=30)
			for t in self.tasks:
				self.taskListText.insert(END, t.getName()+'\n')
			self.taskListText.grid(row=1, column=0, columnspan=4)
			self.editListVisible = TRUE
			print("FALSE")
			self.editButton.config(relief=SUNKEN)
		else:
			self.taskListButton.grid_remove()
			self.taskListText.grid_remove()
			self.editListVisible = FALSE
			self.startButton.grid()
			print("TRUE")
			self.editButton.config(relief=RAISED)

	
	def visualize(self):

		maxWidth = self.winfo_width()


		if not self.visuVisible:
		# create child window
		#visuWin = Toplevel()
		# display message
		#message = "This is the child window"
		#Label(self, text=message).pack()
		# quit child window and return to root window
		# the button is optional here, simply use the corner x of the child window
		#Button(self, text='OK', command=visuWin.destroy).pack()

			self.visuVisible = TRUE
			self.vis = Canvas(self, width=maxWidth, height=400)
			#vis.pack()
			self.vis.grid(row=2,column=0,columnspan=5)


			x0 = 0
			y0 = 0
			h = 30
			w = 0

			allTotal = 0
			for t in self.tasks:
				allTotal = allTotal + t.getTotalTime()

			for t in self.tasks:

				tot = t.getTotalTime()


				for s in t.getSessions():

					if(tot != 0):
						w = (s.getTotalTime()*1.0 / allTotal)*150

					print("\ns.tot: " + str(s.getTotalTime()))
					print("w: " + str(w))
					print("tot: " + str(tot))
					self.vis.create_rectangle(x0, y0, x0+w, y0+h, fill="green")
					x0 = x0+w

				x0 = 0
				y0 = y0 + h + 10
			self.outputButton.config(relief=SUNKEN)
		else:
			self.visuVisible = FALSE
			self.vis.grid_remove()
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






		#self.newTask = IntVar()
		#i = 0
		#for t in self.tasks:
		#	print (t.getName())
		#	Radiobutton(self, text='Task '+str(i), value=i,  variable=self.newTask, indicatoron=0, command=self.start).pack(anchor=W)
		#	i = i+1
		        #t.getName()

		#http://pyinmyeye.blogspot.fi/2012/08/tkinter-combobox-demo.html



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
		app = GUI(root, tasks)

	else:

		tasks = []

		app = GUI(root, tasks)
		app.editList()


	atexit.register(doSomethingOnExit, tasks)
	root.wm_attributes("-topmost", 1)
	root.mainloop()


if __name__ == '__main__':
	main()  
