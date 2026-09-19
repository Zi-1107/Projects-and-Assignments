import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime as dt
import calendar
import to_do_list_file_func as filef 


root = tk.Tk()
root.title("Task Manager")
root.geometry("800x600")
root.state('zoomed')

topframe = tk.Frame(root, padx=100, pady=20)
topframe.pack(fill="x")
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

class CalendarWidget(tk.Toplevel):
    def __init__(self, master, on_date_select, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Select Date")
        self.geometry("250x250")
        self.on_date_select = on_date_select
        
        self.selected_date = None

        self.current_year = dt.now().year
        self.current_month = dt.now().month

        self.header_frame = tk.Frame(self)
        self.header_frame.pack(pady=10)  # Increased padding for header

        self.body_frame = tk.Frame(self)
        self.body_frame.pack()

        self.init_header()
        self.load_calendar(self.current_year, self.current_month)

    def init_header(self):
        # Navigation buttons and label for the month and year
        self.prev_button = tk.Button(self.header_frame, text="<", command=self.prev_month)
        self.prev_button.grid(row=0, column=0)

        self.month_label = tk.Label(self.header_frame, text="", width=12)  # Increased width for padding
        self.month_label.grid(row=0, column=1)

        self.next_button = tk.Button(self.header_frame, text=">", command=self.next_month)
        self.next_button.grid(row=0, column=2)

    def load_calendar(self, year, month):
        # Clear the current calendar
        for widget in self.body_frame.winfo_children():
            widget.destroy()

        # Set the header with the current month and year
        self.month_label.config(text=f"{calendar.month_name[month]} {year}")

        # Weekday headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.body_frame, text=day).grid(row=0, column=i)

        # Generate the calendar for the given month and year
        cal = calendar.monthcalendar(year, month)
        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(self.body_frame, text=str(day), command=lambda d=day: self.select_date(d))
                    btn.grid(row=row_idx + 1, column=col_idx)

    def prev_month(self):
        # Navigate to the previous month
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.load_calendar(self.current_year, self.current_month)

    def next_month(self):
        # Navigate to the next month
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.load_calendar(self.current_year, self.current_month)

    def select_date(self, day):
        # Select a date and return it to the main application
        self.selected_date = dt(self.current_year, self.current_month, day)
        self.on_date_select(self.selected_date.strftime(r"%d-%m-%Y"))
        self.destroy()

def refresh(notebook):
    file_instance = filef.file_func()  # Create an instance of file_func
    file_instance.clean_data_txt()
    tasklist = file_instance.read_file()
    check_instance = filef.check()
    data = check_instance.check_type(tasklist=tasklist)

    n_today = len(data["Today"])
    n_important = len(data["Important"])
    n_completed = len(data["Completed"])
    n_total = len(data["All"])

    tk.Label(topframe, 
            text =f"{n_total}  Total").grid(row=0, column=0, sticky="w", padx=10)
    tk.Label(topframe, 
            text =f"{n_today}  Today").grid(row=1, column=0, sticky="w", padx=10)
    tk.Label(topframe, 
            text =f"{n_important}  Important").grid(row=1, column=1, sticky="w", padx=10)
    tk.Label(topframe, 
            text =f"{n_completed}  Completed").grid(row=0, column=1, sticky="w", padx=10)

    for widget in notebook.winfo_children():
        widget.destroy()

    tabs = {}
    for tab_key, tab_data in data.items():
        tab = TabRows(notebook, tab_key, tab_data)
        notebook.add(tab, text=tab_key)
        tabs[tab_key] = tab


def add_task_win():

    addtask_win = tk.Toplevel(root)

    addtask_win.title("Add New Task")
    addtask_win.geometry("750x280")

    frame = tk.Frame(addtask_win, padx=10, pady=10)
    frame.pack(fill="x")

    validate_len_t = addtask_win.register(lambda text: len(text) <= 35)  # Title limit: 25 characters
    tk.Label(frame, text="Title").grid(row=0, column=0, sticky="w")
    title_entry = tk.Entry(frame, validate="key", validatecommand=(validate_len_t, "%P"), width=40, textvariable = "Task")
    title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    validate_len_d = addtask_win.register(lambda text: len(text) <= 62)  # Description limit: 35 characters
    tk.Label(frame, text="Description").grid(row=1, column=0, sticky="w")
    description_entry = tk.Entry(frame, validate="key", validatecommand=(validate_len_d, "%P"), width=95, textvariable= "Desc")
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

    def open_calendar():
        # Open the calendar widget
        CalendarWidget(root, lambda selected_date: date_label.config(text=f"Date: {selected_date}"))

    tk.Label(frame, text="Date").grid(row=2, column=0, sticky="w")
    default_date = dt.now().strftime(r"%d-%m-%Y")  # Example: Current date as "YYYY-MM-DD"
    date_label = tk.Label(frame, text=f"Date: {default_date}")
    date_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    date_button = tk.Button(frame, text="Pick Date", command=open_calendar) #command to calender
    date_button.grid(row=2, column=2, padx=5, pady=5)

    tk.Label(frame, text="Time (HH:MM)").grid(row=3, column=0, sticky="w")

    time_hour_combobox = ttk.Combobox(frame, state="readonly", values=[f"{hour:02d}" for hour in range(24)], width=3)
    time_hour_combobox.set(f"{dt.today().hour}")
    time_hour_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    time_minute_combobox = ttk.Combobox(frame, state="readonly", values=[f"{minute:02d}" for minute in range(0, 60, 1)], width=3)
    time_minute_combobox.set(f"{dt.today().minute:02d}")
    time_minute_combobox.grid(row=3, column=2, padx=5, pady=5, sticky="w")

    important_var = tk.IntVar()
    tk.Checkbutton(frame, text="Important", variable=important_var).grid(row=5, column=0, sticky="w")

    def retrive_values():
        task_title = title_entry.get()
        task_description = description_entry.get()
        task_date = date_label.cget("text").replace("Date: ", "")
        task_time = f"{time_hour_combobox.get()}:{time_minute_combobox.get()}"
        important = True if important_var.get() > 0 else False
        completed = False

        title_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        date_label.config(text="Date: Not Selected")
        time_hour_combobox.set("")
        time_minute_combobox.set("")
        important_var.set(0)
        addtask_win.destroy()

        return [task_title, task_description, task_date, task_time, important, completed]

    def add_values_file():
        filef_instance = filef.file_func()
        values = retrive_values()
        title, description, date, time, important, completed = values

        if title == "":
            title = "Task"
        if description == "":
            description = "No description"
        # Convert boolean flags to file-compatible symbols
        important_flag = "*" if important else "^"
        completed_flag = "*" if completed else "^"

        filef_instance.add_to_file(title, description, date, time, important_flag, completed_flag)

        refresh(notebook)

    add_button = tk.Button(frame, text="Add Task", command=add_values_file) #command add task to file
    add_button.grid(row=6, column=0, columnspan=3, pady=10)

class TabRows(tk.Frame):
    def __init__(self, root, tab_key, data=None):
        super().__init__(root)
        self.tab_key = tab_key
        self.data = data or []
        self.num_cols = 6  # Default number of columns (Title, Description, Date, Time, Important, Completed)
        self.init_ui()

    def init_ui(self):

        # Add a canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add column headers
        headers = ["Title", "Description", "Date", "Time", "Important", "Completed"]
        header_widths = [50, 85, 40, 15, 10, 10]  # Adjust header widths
        for col_index, (header, width) in enumerate(zip(headers, header_widths)):
            tk.Label(self.scrollable_frame, text=header, anchor="w", width=width).grid(row=0, column=col_index, sticky="w", padx=10)

        # Add rows from data
        self.render_grid()

    def check_completed(self, row_index, row):
        file_instance = filef.file_func()
        title, desc, date, time, important, completed = row
        time = str(time)
        date = date.strftime(r"%d-%m-%Y")
        important_flag = "*" if important else "^"
        completed_flag = "*" if completed else "^"
        file_instance.dlt_task_file(title, desc, date, time[:5], important_flag, completed_flag)
        self.data[row_index].completed = True
        file_instance.add_to_file(title, desc, date, time[:5], important_flag, "*")
        refresh(notebook)
    
    def delete_row(self, row_index):
        # Add a confirmation popup
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
        if confirm:
            # Extract the row data to delete
            task = self.data[row_index]
            title, description, date, time, important, completed = task.title, task.description, task.date.strftime(r"%d-%m-%Y"), str(task.time), task.important, task.completed
            # Convert flags back to their string equivalents for file consistency
            important_flag = "*" if important else "^"
            completed_flag = "*" if completed else "^"

            # Delete from file
            file_instance = filef.file_func()
            file_instance.dlt_task_file(title, description, date, time[:5], important_flag, completed_flag)

            print(title, description, date, time[:5], important_flag, completed_flag)
            # Refresh the UI
            refresh(notebook)


    def render_grid(self):
        # Clear existing widgets in the frame
        for widget in self.winfo_children()[6:]:  # Skip headers
            widget.destroy()

        for row_index, task in enumerate(self.data):
            row = [task.title, task.description, task.date, task.time, task.important, task.completed]
            for col_index, coll in enumerate(row[:-2]):  # Skip Important and Completed for labels
                # Create Label widgets for fixed text cells
                header_widths = [50, 85, 40, 15, 10, 10]
                label = tk.Label(self.scrollable_frame, text=str(coll), anchor="w", width=header_widths[col_index])
                label.grid(row=row_index + 1, column=col_index, padx=5, pady=5)

            # Add Checkbuttons for Important and Completed columns
            important = tk.Label(self.scrollable_frame, text="✔" if row[-2] else "✘", anchor="center", width=header_widths[4])
            important.grid(row=row_index + 1, column=4, padx=0)
            button_text = "✔" if self.data[row_index].completed else "X"
            button = tk.Button(self.scrollable_frame, text=button_text, command=lambda :self.check_completed(row_index, row))
            button.grid(row=row_index + 1, column=5, padx=5)

            # Add Delete button for each row
            delete_button = tk.Button(self.scrollable_frame, text="Delete", command=lambda r=row_index: self.delete_row(r))
            delete_button.grid(row=row_index + 1, column=6, padx=5)


refresh(notebook)

#add task buttton---------------
addtask_btn = tk.Button(topframe, 
             text ="Add New Task", 
             command = add_task_win)
addtask_btn.grid(row=6, column=100, sticky="s")
#add task buttton---------------





#mainloop
root.mainloop()