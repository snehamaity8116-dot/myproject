import sqlite3
from datetime import datetime


db = sqlite3.connect("tasks.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    hid INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    action TEXT,
    time TEXT
)
""")

db.commit()




def add_history(task_id, action):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO history (task_id, action, time) VALUES (?, ?, ?)",
        (task_id, action, time)
    )
    db.commit()




def add_task():
    title = input("Enter task name: ")

    cursor.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        (title, "Pending")
    )

    task_id = cursor.lastrowid
    add_history(task_id, "Task Added")

    db.commit()
    print("Task added successfully.")


def view_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    if not rows:
        print("No tasks found.")
    else:
        print("\nID | Task | Status")
        print("------------------")

        for row in rows:
            print(row[0], "|", row[1], "|", row[2])


def edit_task():
    tid = int(input("Enter Task ID: "))
    new_title = input("Enter new task name: ")

    cursor.execute(
        "UPDATE tasks SET title=? WHERE id=?",
        (new_title, tid)
    )

    if cursor.rowcount == 0:
        print("Task not found.")
    else:
        add_history(tid, "Task Edited")
        db.commit()
        print("Task updated.")


def complete_task():
    tid = int(input("Enter Task ID: "))

    cursor.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (tid,)
    )

    if cursor.rowcount == 0:
        print("Task not found.")
    else:
        add_history(tid, "Task Completed")
        db.commit()
        print("Task marked as completed.")


def delete_task():
    tid = int(input("Enter Task ID: "))

    cursor.execute("DELETE FROM tasks WHERE id=?", (tid,))

    if cursor.rowcount == 0:
        print("Task not found.")
    else:
        add_history(tid, "Task Deleted")
        db.commit()
        print("Task deleted.")


def view_history():
    cursor.execute("SELECT * FROM history")
    rows = cursor.fetchall()

    if not rows:
        print("No history found.")
    else:
        print("\nID | Task ID | Action | Time")
        print("-----------------------------")

        for row in rows:
            print(row[0], "|", row[1], "|", row[2], "|", row[3])


# ======================
# Main Menu
# ======================

while True:

    print("\n===== Task Manager =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Edit Task")
    print("4. Complete Task")
    print("5. Delete Task")
    print("6. View History")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        edit_task()

    elif choice == "4":
        complete_task()

    elif choice == "5":
        delete_task()

    elif choice == "6":
        view_history()

    elif choice == "7":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")

