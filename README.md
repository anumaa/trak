# trak

Minimalistic tool for task-based time tracking (version 0.1, so minor and major tweaks will probably be happening soon)

Usage: 
>python trak.py  
(>python3 trak.py) 

Tasks are added by writing one task per line onto a text box. Deleting a task from the list will archive it - it will no longer be presented on the user interface or reporting, but can be reactivated by typing it up again onto the list (use cases and user interface for dealing with the archived tasks will need some further consideration) 

The app is set to stay on top of all other windows, and is small enough to fit to a corner of a screen, for easy access to switch tasks whenever necessary. The currently active task is selected from a dropdown menu, and can be paused during breaks - no time is counted during the pause. When a new task is chosen from the menu, it becomes active and its time is being counted (and the previously active task time is no longer counted). 

Reporting currently includes a visual overview (and cumulative time) per task for the ongoing week. The same information can also be exported in CSV format for easy importing to spreadsheet programs. (reporting is rudimentary at this stage, it will be improved according to the user wishes and needs during the upcoming weeks) 

Data persistence is currently handlded with Python's pickle serialization, but database or cloud storage might be better for data consistency. Developing a corresponding web application is another possible future endeavour. 


TODO: 
-specifying visualization and reporting to meet the user needs
-handling multiple projects ("clients"), each with multiple tasks
-offering UI to visualize and report past tasks / over different time periods 
-user interfaces / use cases for reactivating archived tasks
-data persistence, web version 
