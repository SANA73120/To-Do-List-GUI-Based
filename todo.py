# -----------------------------
# Import the required libraries
# -----------------------------
import tkinter as tk                  # Tkinter for GUI (Graphical User Interface)
from tkinter import messagebox, simpledialog  # For pop-up boxes
import json                           # To save/load tasks in a file
import os                             # To check if file exists

# -----------------------------
#Functions to handle saving/loading tasks
# -----------------------------
def save_tasks(tasks):
    """
    Save the list of tasks to a JSON file (tasks.json).
    JSON is a format that stores data like a dictionary/list.
    """
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)  # indent=4 makes the file look pretty

def load_tasks():
    """
    Load tasks from the JSON file if it exists.
    If no file exists, return an empty list [].
    """
    if not os.path.exists("tasks.json"):  # If file not found
        return []
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)           # Load existing tasks
    except json.JSONDecodeError:          # If file is empty or broken
        return []

# -----------------------------
#Main To-Do App Class
# -----------------------------
class TodoApp:
    def __init__(self, root):
        #Window settings
        self.root = root
        self.root.title("✨ To-Do List ✨")   # Title of the window
        self.root.geometry("550x550")              # Set size of window
        self.root.config(bg="#f0f8ff")             # Light blue background

        #Load tasks from file
        self.tasks = load_tasks()

        #Title Label (Header at top)
        tk.Label(
            root,
            text="📋 To-Do List",
            font=("Arial", 20, "bold"),   # Font style
            bg="#4682b4",                 # Steel Blue background
            fg="white",                   # White text
            pady=10                       # Padding on top and bottom
        ).pack(fill="x")                  # Stretch label across window

        #Listbox where tasks will be displayed
        self.task_listbox = tk.Listbox(
            root,
            width=60,             # Width of the box
            height=15,            # Height in number of rows
            bg="#fafad2",         # Light golden background
            fg="black",           # Black text
            font=("Arial", 12),   # Font style
            selectbackground="#87ceeb",  # Highlight color when selecting task
        )
        self.task_listbox.pack(pady=15)   # Add some space around
        self.refresh_tasks()              # Show tasks

        #Buttons for actions
        btn_frame = tk.Frame(root, bg="#f0f8ff")  # Frame to keep buttons together
        btn_frame.pack(pady=10)

        #Add Task button
        tk.Button(
            btn_frame, text="➕ Add Task", width=12,
            bg="#32cd32", fg="white", command=self.add_task
        ).grid(row=0, column=0, padx=5)

        #Mark Done button
        tk.Button(
            btn_frame, text="✅ Mark Done", width=12,
            bg="#1e90ff", fg="white", command=self.complete_task
        ).grid(row=0, column=1, padx=5)

        #Delete Task button
        tk.Button(
            btn_frame, text="🗑️ Delete Task", width=12,
            bg="#ff6347", fg="white", command=self.delete_task
        ).grid(row=0, column=2, padx=5)

        #Save & Exit button
        tk.Button(
            root, text="💾 Save & Exit", width=20,
            bg="#8a2be2", fg="white", command=self.exit_app
        ).pack(pady=15)

    # -----------------------------
    #Refresh task list display
    # -----------------------------
    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)  # Clear the listbox
        for task in self.tasks:
            # Show ✔️ if done, ❌ if not done
            status = "✔️" if task["done"] else "❌"
            self.task_listbox.insert(tk.END, f"{task['title']} - {status}")

    # -----------------------------
    #Add a new task
    # -----------------------------
    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task name:")
        if title:  # If user typed something
            self.tasks.append({"title": title, "done": False})  # Save as not done
            self.refresh_tasks()

    # -----------------------------
    #Mark task as completed
    # -----------------------------
    def complete_task(self):
        selected = self.task_listbox.curselection()  # Get selected task index
        if not selected:  # If nothing is selected
            messagebox.showwarning("Warning", "⚠️ Please select a task.")
            return
        self.tasks[selected[0]]["done"] = True  # Mark as done
        self.refresh_tasks()

    # -----------------------------
    # Delete a task
    # -----------------------------
    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "⚠️ Please select a task.")
            return
        self.tasks.pop(selected[0])  # Remove from list
        self.refresh_tasks()

    # -----------------------------
    # Save and close the app
    # -----------------------------
    def exit_app(self):
        save_tasks(self.tasks)  # Save tasks to file
        messagebox.showinfo("Exit", "💾 Tasks saved. Goodbye!")  # Inform user
        self.root.quit()  # Close window


# -----------------------------
# Run the application
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()         # Create main window
    app = TodoApp(root)    # Run the app
    root.mainloop()        # Keep the window open
