# Connor Ronan - Capstone Project Task Manager
import os
from datetime import datetime

# Figure out where this script is saved, so we can find the text files
script_folder = os.path.dirname(os.path.abspath(__file__))

# Try both the script's folder and the current working folder
# (this makes the program work no matter where you run it from)


def find_file(filename):
    option1 = os.path.join(script_folder, filename)
    option2 = os.path.join(os.getcwd(), filename)
    if os.path.exists(option1):
        return option1
    elif os.path.exists(option2):
        return option2
    else:
        # Return the first option anyway so we still get a FileNotFoundError
        return option1


user_file = find_file("user.txt")
tasks_file = find_file("tasks.txt")
task_overview_file = os.path.join(script_folder, "task_overview.txt")
user_overview_file = os.path.join(script_folder, "user_overview.txt")


# ===== Loading and saving files ===========

def load_users():
    # Reads usernames and passwords from user.txt into a dictionary
    users = {}
    try:
        with open(user_file, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    username, password = line.split(", ")
                    users[username] = password
    except FileNotFoundError:
        print(f"Error: user.txt not found. Looked here: {user_file}")
    return users


def save_users(users):
    # Writes the users dictionary back to user.txt
    with open(user_file, "w") as file:
        for username, password in users.items():
            file.write(f"{username}, {password}\n")


def load_tasks():
    # Reads tasks from tasks.txt into a list of dictionaries
    tasks = []
    try:
        with open(tasks_file, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    task = {
                        "user": parts[0],
                        "title": parts[1],
                        "description": parts[2],
                        "assigned_date": parts[3],
                        "due_date": parts[4],
                        "completed": parts[5]
                    }
                    tasks.append(task)
    except FileNotFoundError:
        print(f"Error: tasks.txt not found. Looked here: {tasks_file}")
    return tasks


def save_tasks(tasks):
    # Writes the task list back to tasks.txt
    with open(tasks_file, "w") as file:
        for t in tasks:
            file.write(
                f"{t['user']}, {t['title']}, {t['description']}, "
                f"{t['assigned_date']}, {t['due_date']}, "
                f"{t['completed']}\n"
            )


# ===== Menu functions ===========

def reg_user(users):
    # Only admin can register users
    new_user = input("Enter a new username: ")

    # Don't allow duplicate usernames
    if new_user in users:
        print("That username already exists, try another one.\n")
        return users

    new_pass = input("Enter a new password: ")
    confirm = input("Confirm the password: ")

    if new_pass == confirm:
        users[new_user] = new_pass
        save_users(users)
        print(f"User '{new_user}' has been registered.\n")
    else:
        print("The passwords do not match. User not registered.\n")
    return users


def add_task(tasks):
    # Asks the user for the task details
    username = input("Who is the task assigned to? ")
    title = input("What is the title of the task? ")
    description = input("Give a description of the task: ")
    due_date = input("What is the due date? (e.g. 25 Oct 2026) ")

    # Get today's date in the same format as tasks.txt
    today = datetime.now().strftime("%d %b %Y")

    task = {
        "user": username,
        "title": title,
        "description": description,
        "assigned_date": today,
        "due_date": due_date,
        "completed": "No"
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added and assigned to {username}.\n")
    return tasks


def view_all(tasks):
    # Shows every task in a readable format
    if not tasks:
        print("No tasks to show.\n")
        return

    for i, t in enumerate(tasks, start=1):
        print(f"--- Task {i} ---")
        print(f"Task:           {t['title']}")
        print(f"Assigned to:    {t['user']}")
        print(f"Date assigned:  {t['assigned_date']}")
        print(f"Due date:       {t['due_date']}")
        print(f"Task complete?  {t['completed']}")
        print(f"Description:    {t['description']}")
        print()


def view_mine(current_user, tasks):
    # Shows only the tasks assigned to the logged-in user
    my_tasks = []
    for i, t in enumerate(tasks):
        if t["user"] == current_user:
            my_tasks.append((i, t))

    if not my_tasks:
        print("You have no tasks assigned to you.\n")
        return tasks

    # Show them with a number next to each
    for number, (index, t) in enumerate(my_tasks, start=1):
        print(f"--- Task {number} ---")
        print(f"Task:           {t['title']}")
        print(f"Assigned to:    {t['user']}")
        print(f"Date assigned:  {t['assigned_date']}")
        print(f"Due date:       {t['due_date']}")
        print(f"Task complete?  {t['completed']}")
        print(f"Description:    {t['description']}")
        print()

    # Let the user pick a task, or -1 to go back
    choice = input(
        "Enter a task number to edit, or -1 to return to the menu: "
    )

    if choice == "-1":
        return tasks

    try:
        choice = int(choice)
    except ValueError:
        print("That's not a valid number.\n")
        return tasks

    if choice < 1 or choice > len(my_tasks):
        print("That task number doesn't exist.\n")
        return tasks

    # Get the actual task from the main list
    real_index = my_tasks[choice - 1][0]
    task = tasks[real_index]

    print("What do you want to do with this task?")
    print("1 - Mark it as complete")
    print("2 - Edit the task")
    action = input("Enter 1 or 2: ")

    if action == "1":
        task["completed"] = "Yes"
        save_tasks(tasks)
        print("Task has been marked as complete.\n")

    elif action == "2":
        # Can only edit if it hasn't been completed yet
        if task["completed"] == "Yes":
            print("This task is already complete and cannot be edited.\n")
            return tasks

        print("Leave blank to keep the current value.")
        new_user = input(f"Assigned user ({task['user']}): ")
        new_due = input(f"Due date ({task['due_date']}): ")

        if new_user:
            task["user"] = new_user
        if new_due:
            task["due_date"] = new_due

        save_tasks(tasks)
        print("Task has been updated.\n")

    else:
        print("That's not a valid option.\n")

    return tasks


def view_completed(tasks):
    # Admin only: shows all completed tasks
    completed = []
    for t in tasks:
        if t["completed"] == "Yes":
            completed.append(t)

    if not completed:
        print("No completed tasks yet.\n")
        return

    for i, t in enumerate(completed, start=1):
        print(f"--- Completed Task {i} ---")
        print(f"Task:           {t['title']}")
        print(f"Assigned to:    {t['user']}")
        print(f"Date assigned:  {t['assigned_date']}")
        print(f"Due date:       {t['due_date']}")
        print(f"Task complete?  {t['completed']}")
        print(f"Description:    {t['description']}")
        print()


def delete_task(tasks):
    # Admin only: lets the admin delete a task
    if not tasks:
        print("No tasks to delete.\n")
        return tasks

    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t['title']} (assigned to {t['user']})")

    choice = input("Enter the number of the task you want to delete: ")

    try:
        choice = int(choice)
    except ValueError:
        print("That's not a valid number.\n")
        return tasks

    if choice < 1 or choice > len(tasks):
        print("That task doesn't exist.\n")
        return tasks

    removed = tasks.pop(choice - 1)
    save_tasks(tasks)
    print(f"Task '{removed['title']}' has been deleted.\n")
    return tasks


def generate_reports(tasks, users):
    # Total counts
    total_tasks = len(tasks)

    completed = 0
    for t in tasks:
        if t["completed"] == "Yes":
            completed += 1

    uncompleted = total_tasks - completed

    # Work out how many are overdue (not completed and due date is in the past)
    today = datetime.now()
    overdue = 0

    for t in tasks:
        if t["completed"] == "No":
            try:
                due = datetime.strptime(t["due_date"], "%d %b %Y")
                if due < today:
                    overdue += 1
            except ValueError:
                pass

    # Percentages
    if total_tasks > 0:
        pct_incomplete = (uncompleted / total_tasks) * 100
        pct_overdue = (overdue / total_tasks) * 100
    else:
        pct_incomplete = 0
        pct_overdue = 0

    # Write task_overview.txt
    with open(task_overview_file, "w") as file:
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed}\n")
        file.write(f"Uncompleted tasks: {uncompleted}\n")
        file.write(f"Overdue and uncompleted: {overdue}\n")
        file.write(f"Percentage incomplete: {pct_incomplete:.2f}%\n")
        file.write(f"Percentage overdue: {pct_overdue:.2f}%\n")

    # Write user_overview.txt
    total_users = len(users)
    with open(user_overview_file, "w") as file:
        file.write(f"Total users: {total_users}\n")
        file.write(f"Total tasks: {total_tasks}\n\n")

        for username in users:
            # Get this user's tasks
            user_tasks = []
            for t in tasks:
                if t["user"] == username:
                    user_tasks.append(t)

            num_user_tasks = len(user_tasks)

            if total_tasks > 0:
                pct_of_all = (num_user_tasks / total_tasks) * 100
            else:
                pct_of_all = 0

            user_completed = 0
            for t in user_tasks:
                if t["completed"] == "Yes":
                    user_completed += 1

            user_incomplete = num_user_tasks - user_completed

            if num_user_tasks > 0:
                pct_user_completed = (user_completed / num_user_tasks) * 100
                pct_user_incomplete = (user_incomplete / num_user_tasks) * 100
            else:
                pct_user_completed = 0
                pct_user_incomplete = 0

            user_overdue = 0
            for t in user_tasks:
                if t["completed"] == "No":
                    try:
                        due = datetime.strptime(t["due_date"], "%d %b %Y")
                        if due < today:
                            user_overdue += 1
                    except ValueError:
                        pass

            if num_user_tasks > 0:
                pct_user_overdue = (user_overdue / num_user_tasks) * 100
            else:
                pct_user_overdue = 0

            file.write(f"User: {username}\n")
            file.write(f"  Total tasks: {num_user_tasks}\n")
            file.write(
                f"  Percentage of all tasks: {pct_of_all:.2f}%\n"
            )
            file.write(f"  Completed: {pct_user_completed:.2f}%\n")
            file.write(f"  Still to complete: {pct_user_incomplete:.2f}%\n")
            file.write(
                f"  Overdue and incomplete: {pct_user_overdue:.2f}%\n\n"
            )

    print("Reports have been created.\n")


def display_statistics(tasks, users):
    # If the reports don't exist yet, make them first
    if (
        not os.path.exists(task_overview_file)
        or not os.path.exists(user_overview_file)
    ):
        generate_reports(tasks, users)

    print("\n===== Task Overview =====")
    with open(task_overview_file, "r") as file:
        print(file.read())

    print("===== User Overview =====")
    with open(user_overview_file, "r") as file:
        print(file.read())


# ===== Login ===========

users = load_users()
tasks = load_tasks()

current_user = None

while current_user is None:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username] == password:
        current_user = username
        print(f"\nWelcome, {username}!\n")
    else:
        print("That username or password isn't right. Try again.\n")


# ===== Main menu ===========

while True:
    # Admin gets extra options
    if current_user == "admin":
        menu = input(
            '''Please select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete a task
gr - generate reports
ds - display statistics
e - exit
: '''
        ).lower()
    else:
        menu = input(
            '''Please select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: '''
        ).lower()

    if menu == "r":
        if current_user == "admin":
            users = reg_user(users)
        else:
            print("Only admin can register users.\n")

    elif menu == "a":
        tasks = add_task(tasks)

    elif menu == "va":
        view_all(tasks)

    elif menu == "vm":
        tasks = view_mine(current_user, tasks)

    elif menu == "vc":
        if current_user == "admin":
            view_completed(tasks)
        else:
            print("Only admin can view completed tasks.\n")

    elif menu == "del":
        if current_user == "admin":
            tasks = delete_task(tasks)
        else:
            print("Only admin can delete tasks.\n")

    elif menu == "gr":
        if current_user == "admin":
            generate_reports(tasks, users)
        else:
            print("Only admin can generate reports.\n")

    elif menu == "ds":
        if current_user == "admin":
            display_statistics(tasks, users)
        else:
            print("Only admin can display statistics.\n")

    elif menu == "e":
        print("Goodbye!")
        break

    else:
        print("That's not a valid option. Try again.\n")
