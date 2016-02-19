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
		#self.wm_protocol("WM_DELETE_WINDOW", self.onExit)


	def loadTasks(self, tasks):
		self.tasks = tasks


	def onExit(self):
		print('onExit')
		#pickle
		self.destroy()

	def start(self, event):

		print("current: " + str(self.taskList.current()))
		self.stopButton.config(relief=RAISED)
		self.startButton.config(relief=SUNKEN)
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
		
		
	
	def stop(self):
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
		# create child window
		#visuWin = Toplevel()
		# display message
		#message = "This is the child window"
		#Label(self, text=message).pack()
		# quit child window and return to root window
		# the button is optional here, simply use the corner x of the child window
		#Button(self, text='OK', command=visuWin.destroy).pack()

		vis = Canvas(self, width=400, height=250)
		#vis.pack()
		vis.grid(row=2,column=0)



		#vis.create_rectangle(50, 20, 150, 80, fill="#476042")
		##w.create_rectangle(65, 35, 135, 65, fill="yellow")
		#w.create_line(0, 0, 50, 20, fill="#476042", width=3)
		#w.create_line(0, 100, 50, 80, fill="#476042", width=3)
		#w.create_line(150,20, 200, 0, fill="#476042", width=3)
		#w.create_line(150, 80, 200, 100, fill="#476042", width=3)

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
				vis.create_rectangle(x0, y0, x0+w, y0+h, fill="green")
				x0 = x0+w

			x0 = 0
			y0 = y0 + h + 10

				#vis.create_rectangle(10,10,150,150,fill='black')



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

		self.pack(fill=BOTH, expand=True)
		self.var = BooleanVar()

		taskNames = []
		for t in self.tasks:
			taskNames.append(t.getName())




		self.newTask = StringVar()
		self.taskList = ttk.Combobox(self, textvariable=self.newTask, values=taskNames)

		#self.taskList['values'] = taskNames
		self.taskList.bind('<<ComboboxSelected>>',self.start)
		#self.taskList.place(x='0', y='0')
		#self.taskList.current(0)
		self.taskList.grid(row=0,column=0)
		#self.taskList.pack(side=LEFT)

		print(self.newTask)


		self.playImg = PhotoImage(file='images/play.png')
		self.startButton = Button(self, justify = LEFT, command = self.start, image=self.playImg)
		#self.startButton.place(x=50, y=0)
		#self.startButton.pack(side=LEFT)
		self.startButton.grid(row=0,column=1)

		self.pauseImg = PhotoImage(file='images/pause.png')
		self.stopButton = Button(self, justify = LEFT, command = self.stop, image=self.pauseImg)
		#self.stopButton.place(x=86, y=0)
		#self.stopButton.pack(side=LEFT)
		self.stopButton.grid(row=0,column=2)

		self.ejectImg = PhotoImage(file='images/eject.png')
		self.editButton = Button(self, justify = LEFT, command=self.editList, image=self.ejectImg)
		#self.editButton.place(x=122, y=0)
		#self.editButton.pack(side=LEFT)
		self.editButton.grid(row=0,column=3)

		self.outputImg = PhotoImage(file='images/menu-lines.png')
		self.outputButton = Button(self, justify = LEFT, command=self.visualize, image=self.outputImg)
		#self.editButton.place(x=122, y=0)
		#self.editButton.pack(side=LEFT)
		self.outputButton.grid(row=0,column=4)



		#self.visuButton = Button(self, text="VISU", command = self.visualize)
		#self.visuButton.place(x=150, y = 90)
		
		
		#self.printButton = Button(self, text="PRINT", command = self.printAll)
		#self.printButton.place(x=500	, y=300)

		#self.newTask = IntVar()
		#i = 0
		#for t in self.tasks:
		#	print (t.getName())
		#	Radiobutton(self, text='Task '+str(i), value=i,  variable=self.newTask, indicatoron=0, command=self.start).pack(anchor=W)
		#	i = i+1
		        #t.getName()




		#http://pyinmyeye.blogspot.fi/2012/08/tkinter-combobox-demo.html
		#todo add to list
		#cb1 = ttk.Combobox(self)
		#cb1.bind('<Return>', self.updateList)
		#cb1.pack(pady=5, padx=10)
        
		#Radiobutton(self, text="One", value=1).pack(anchor=W)
		#Radiobutton(self, text="Two", value=2).pack(anchor=W)



		#startButton = Button(self, text="START", command=self.start)
		#startButton.place(x=50, y=50)

		#cb = Checkbutton(self, text="Show title",
		#    variable=self.var, command=self.onClick)
		#cb.select()
		#cb.place(x=50, y=50)



	#def closeEvent(self):
	#	print ("exit handler")
	#	self.destroy()

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
		#root.geometry("250x150+300+300")
		#app.loadTasks(tasks)

		#root.protocol( "WM_DELETE_WINDOW", closeMe )



	#init tasks
	else:

		tasks = []

		app = GUI(root, tasks)
		#app.loadTasks(tasks)
		app.editList()

	#print('loaded tasks: ')
	#for t in loadedTasks:
	#	print(t.getName())

	atexit.register(doSomethingOnExit, tasks)
	root.mainloop()





if __name__ == '__main__':
	main()  
