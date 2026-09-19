#24 hour system, * for true - ^ for false, example for datetime: 2024-12-01 19:15:00
#title ~ description ~ date ~ time ~ important_flag ~ completed_flag
import datetime as dt
import calendar
import tkinter as tk
grouplist = ["All", "Today", "Important", "Completed"]
FILENAME = r"to-do list\to_do_list_data.txt"

class Task():
    def __init__(self, title, description, date, time, important, completed) -> None:
        self.title = title if title.strip() else "Task"
        self.description = description if description.strip() else "Description"
        self.date = dt.datetime.strptime(date.strip(), "%d-%m-%Y").date()
        self.time = dt.datetime.strptime(time.strip(), "%H:%M").time()
        self.important = important.strip() == "*"
        self.completed = completed.strip() == "*"  
    
class file_func():
    def __init__(self):
        self.filename = FILENAME

    def read_file(self):
        tasklist = []
        self.clean_data_txt()
        with open(self.filename, "r") as myfile:
            lines = myfile.readlines()
            for line in lines:
                data = line.strip().split(sep=" ~ ")
                #title ~ description ~ date ~ time ~ important_flag ~ completed_flag
                tasklist.append(Task(data[0], data[1], data[2], data[3], data[4], data[5]))

        return tasklist
    
    def add_to_file(self, title, description, date, time, important, completed):
        try:
            with open(self.filename, "a") as myfile:
                myfile.write("\n" + title + " ~ " + description + " ~ " + date + " ~ " + time + " ~ " + important + " ~ " + completed)
        except Exception as e:
            print(f"Error adding task: {e}")

    def dlt_task_file(self, title, description, date, time, important, completed):
        # Construct the string to match for deletion
        str_to_dlt = f"{title} ~ {description} ~ {date} ~ {time} ~ {important} ~ {completed}".strip()
        try:
            with open(self.filename, "r") as myfile:
                lines = myfile.readlines()
            # Remove the line matching the string
            remaining_lines = [line for line in lines if line.strip() != str_to_dlt]
            with open(self.filename, "w") as myfile:
                myfile.writelines(remaining_lines)
        except Exception as e:
            print(f"Error deleting task: {e}")

    def clean_data_txt(self):
        with open(self.filename, "r") as myfile:
            lines = myfile.readlines()
        cleaned_lines = [line for line in lines if line.strip()]
        cleaned_text = "".join(cleaned_lines)
        with open(self.filename, "w") as myfile:
                myfile.writelines(cleaned_text)
    
class check():
    def __init__(self) -> None:
        pass


    def check_important(self, tasklist):
        return [task for task in tasklist if task.important]

    def check_completed(self, tasklist):
        return [task for task in tasklist if task.completed]

    def check_all(self, tasklist):
        return [task for task in tasklist if not task.completed]

    def check_today(self, tasklist):
        today = dt.date.today()
        return [task for task in tasklist if task.date == today]

    def check_type(self, tasklist):
        return {
            "All": self.check_all(tasklist),
            "Completed": self.check_completed(tasklist),
            "Important": self.check_important(tasklist),
            "Today": self.check_today(tasklist),
        }
