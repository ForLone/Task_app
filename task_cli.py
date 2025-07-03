import json
import sys
from datetime import datetime
import os 

class IndexNotFound(Exception):
    # Raised when index not found
    pass

class App():
    def __init__(self):
        self.tasks_data = {}
        self.task_id = 0

    def add(self, task):
        # Adding a new task
        self.task_id+=1
        time = datetime.now().strftime("Created: %m/%d/%Y, %H:%M:%S")
        self.tasks_data[self.task_id] = [task, time, ""]
        print(f"Task added successfully (ID: {self.task_id})")

    def update(self, task_id, task):
        #updating tasks
        if int(sys.argv[2])<=0 or int(sys.argv[2]) > task_id:
            raise IndexNotFound
        updated = datetime.now().strftime("Updated: %m/%d/%Y, %H:%M:%S")
        self.tasks_data[task_id] = [task, updated, self.tasks_data[task_id][-1]]

    def delete(self, task_id):
        #deleting tasks
        if int(sys.argv[2])<=0 or int(sys.argv[2]) > app.task_id:
            raise IndexNotFound
        self.tasks_data.pop(task_id)
        self.task_id-=1
        if self.task_id:
            new_dict = {key:value for key, value in enumerate(self.tasks_data.values(), start=1)}
            self.tasks_data = new_dict


    def mark_in_progress(self, task_id):
        #Marking a task as in progress
        if int(sys.argv[2])<=0 or int(sys.argv[2]) > app.task_id:
            raise IndexNotFound
        self.tasks_data[task_id][-1] = "in_progress"

    def mark_done(self, task_id):
        #Marking a task as done
        if int(sys.argv[2])<=0 or int(sys.argv[2]) > app.task_id:
            raise IndexNotFound
        self.tasks_data[task_id][-1] = "done"

    def all_tasks(self):
        # Listing all tasks
        for key, value in self.tasks_data.items():
            print(key, *value[:3])

    def all_done(self):
        # Listing all done tasks
        for key, value in self.tasks_data.items():
            if value[-1] == "done":
                print(key, *value[:1])

    def all_todo(self):
        # Listing all todo tasks
        for key, value in self.tasks_data.items():
            if not value[-1]:
                print(key, *value[:1])

    def all_in_progress(self):
        # Listing all in progress tasks
        for key, value in self.tasks_data.items():
            if value[-1] == "in_progress":
                print(key, *value[:1])

    def save_tasks(self):
        #saving tasks
        with open("tasks.json", mode="w", encoding="utf-8") as f:
            json.dump(self.tasks_data, f)

    def load_from_file(self):
        #load tasks from file
        if not os.path.isfile("tasks.json"):
            with open("tasks.json", mode="w", encoding="utf-8") as f:
                f.write("{}")
        with open("tasks.json", mode="r", encoding="utf-8") as f:
            self.tasks_data = json.load(f)
        if self.tasks_data:
            new_dict = {int(key):value for key, value in self.tasks_data.items()}
            self.tasks_data = new_dict
            self.task_id = list(self.tasks_data)[-1]

app = App()
app.load_from_file()
commands = ["add", "update", "delete", "mark-in-progress", "mark-done", "list"]
#use list of commands in terminal with: python task-cli.py ... 
list_commands = ["done", "todo", "in-progress"]
#list_commands for "list" command: python task-cli.py list ...
try:
    if sys.argv[1] not in commands:
        print("Command not found")
    if sys.argv[1] == "add":
        app.add(sys.argv[2])
        app.save_tasks()
    if sys.argv[1] == "update":
        app.update(int(sys.argv[2]), sys.argv[3])
        app.save_tasks()
    if sys.argv[1] == "delete":
        app.delete(int(sys.argv[2]))
        app.save_tasks()
    if sys.argv[1] == "mark-in-progress":
        app.mark_in_progress(int(sys.argv[2]))
        app.save_tasks()
    if sys.argv[1] == "mark-done":
        app.mark_done(int(sys.argv[2]))
        app.save_tasks()

    if sys.argv[1] == "list":
        if len(sys.argv) > 3:
            print("Too much arguments")
        elif len(sys.argv) == 3:
            if sys.argv[2] not in list_commands:
                print("Command not found")
            status = sys.argv[2].lower()
            if status == "done":
                app.all_done()
            elif status == "todo":
                app.all_todo()
            elif status == "in-progress":
                app.all_in_progress()
        else:
            app.all_tasks()
except IndexError:
    print("Not enough arguments")
except IndexNotFound:
    print("Index not found")
except ValueError:
    print("Please enter numbers")
