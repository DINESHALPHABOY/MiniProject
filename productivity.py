import tkinter as tk
import sqlite3


# Function to create the SQLite database and table
def create_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER)")
    conn.commit()
    conn.close()


# Function to add a task to the database
def add_daily_task():
    task = task_entry.get()
    if task and len(task_list) <= 10:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO tasks (id,task, completed) VALUES (?,?, ?)", (0,task, 0))
        cursor.execute("INSERT INTO tasks (task) VALUES ( ?)", ( task ))

        conn.commit()
        conn.close()
        update_task_list()
        task_entry.delete(0, tk.END)


# Function to remove a task from the database
def remove_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    update_task_list()


# Function to update a task in the database
def update_task(task_id, new_task_text):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task=? WHERE id=?", (new_task_text, task_id))
    conn.commit()
    conn.close()
    update_task_list()


# Function to update the task list
def update_task_list():
    for widget in task_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    for i, task in enumerate(tasks):
        completed = task[1] == 1
        task_text = task[1]

        # Task text entry field
        task_entry_field = tk.Entry(task_frame, width=20)
        task_entry_field.insert(tk.END, task_text)
        task_entry_field.grid(row=i, column=0)

        # Update button
        update_button = tk.Button(task_frame, text="Update",
                                  command=lambda t=task[0], entry=task_entry_field: update_task(t, entry.get()))
        update_button.grid(row=i, column=1)

        # Remove button
        remove_button = tk.Button(task_frame, text="Remove", command=lambda t=task[0]: remove_task(t))
        remove_button.grid(row=i, column=2)

        # Checkbox
        task_checkbox_var = tk.IntVar()
        task_checkbox = tk.Checkbutton(task_frame, variable=task_checkbox_var)
        task_checkbox.grid(row=i, column=3)

        task_list.append((task[0], task_text, task_checkbox_var))


# Function to calculate productivity
def calculate_productivity():
    completed_tasks = sum(1 for task in task_list if task[2].get())

    if completed_tasks <= 5:
        productivity_label.config(text=f"Productivity Level: Low ({completed_tasks} tasks completed)")
    elif 6 <= completed_tasks <= 7:
        productivity_label.config(text=f"Productivity Level: Better ({completed_tasks} tasks completed)")
    elif 8 <= completed_tasks <= 10:
        productivity_label.config(text=f"Productivity Level: Excellent ({completed_tasks} tasks completed)")


# Create the main window
root = tk.Tk()
root.title("TaskHub: Your Daily Productivity Companion")

# Create the database and table if they don't exist
create_database()

# Task Entry
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

# "Add daily task" Button
add_button = tk.Button(root, text="Add daily task", command=add_daily_task)
add_button.pack()

# Task Frame to display tasks with checkboxes
task_frame = tk.Frame(root)
task_frame.pack()

# Productivity Button
productivity_button = tk.Button(root, text="Calculate Productivity", command=calculate_productivity)
productivity_button.pack()

# Label to display productivity
productivity_label = tk.Label(root, text="")
productivity_label.pack()

# List to store task data (id, text, checkbox variable)
task_list = []

# Update the task list initially
update_task_list()

# Start the GUI main loop
root.mainloop()

