#!/usr/bin/python


from Tkinter import *

from project import * 
from task import * 


class GUI(Frame):




	def __init__(self, parent, tasks):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.tasks = tasks
		self.initUI()
		self.previousTask = -1
    
    
	def start(self):
		
		#print "previous: " + str(self.previousTask)
		if(self.previousTask != -1): 
			self.stop()
		whichTask = self.newTask.get()
		#print "which: " + str(whichTask)
		
		task = self.tasks[whichTask]
		taskTime = str(task.getTotalTime()) 
		
		print 'START ' + str(task.__str__('red')) + "SESSION " + str(len(self.tasks[whichTask].getSessions())+1) + " " + taskTime  
		self.tasks[whichTask].startSession()
		self.previousTask = whichTask
		
		
	
	def stop(self):
		self.tasks[self.previousTask].endSession() 
		print 'STOP  ' + str(self.tasks[self.previousTask].strLatestSession())
		
		
	def printAll(self):
		for t in self.tasks: 
			print t.getName() + " TOTAL: " + str(t.getTotalTime())
			i = 1 
			for s in t.getSessions(): 
				print "\tSESSION " + str(i) + ": " + str(s.getTotalTime())
				#print time.strftime('%H:%M:%S', time.localtime(s.getTotalTime()))
				i = i + 1
	
	
	
	def initUI(self):

		self.parent.title("trak v0.1")

		self.pack(fill=BOTH, expand=True)
		self.var = BooleanVar()

		startButton = Button(self, text="START", command = self.start)
		startButton.place(x=50, y=50)

		stopButton = Button(self, text="STOP", command = self.stop)
		stopButton.place(x=150, y=50)
		
		
		printButton = Button(self, text="PRINT", command = self.printAll)
		printButton.place(x=150, y=70)

		self.newTask = IntVar()
		i = 0
		for t in self.tasks: 
			print t.getName()
			Radiobutton(self, text='Task '+str(i), value=i,  variable=self.newTask, indicatoron=0, command=self.start).pack(anchor=W)
			i = i+1
		        #t.getName()
        
		#Radiobutton(self, text="One", value=1).pack(anchor=W)
		#Radiobutton(self, text="Two", value=2).pack(anchor=W)



		#startButton = Button(self, text="START", command=self.start)
		#startButton.place(x=50, y=50)

		#cb = Checkbutton(self, text="Show title",
		#    variable=self.var, command=self.onClick)
		#cb.select()
		#cb.place(x=50, y=50)
        



def main():

	#init tasks 
	tasks = []
	for i in range(0,5): 
		tname = 'task'+str(i)
		t = Task(tname) 
		tasks.append(t)


	root = Tk()
	root.geometry("250x150+300+300")
	app = GUI(root, tasks)
    

		
	root.mainloop()  


if __name__ == '__main__':
	main()  
