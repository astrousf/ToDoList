import json

def save_to_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file)

def load_from_file(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

users = load_from_file("users.json")
tasks = load_from_file("tasks.json")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return user
    else:
        print("Invalid user!")
    return

def add_user():
    username = input("Enter your username: ")
    if any(user["username"] == username for user in users):
        print("User already exists!")
        return
    password = input("Enter your password: ")
    role = input("Enter role (admin/user): ")
    users.append({"username": username, "password": password, "role": role})
    save_to_file("users.json", users)
    print("User added successfully!")

def delete_user():
    username = input("Enter username to delete: ")
    global users
    for user in users:
        if user["username"] == username:
            users.remove(user)
            save_to_file("users.json", users)
            print(f"User '{username}' deleted successfully!")
            return
    print(f"User '{username}' does not exist!")

def view_users():
    for user in users:
        print(f"Username: {user['username']}, Role: {user['role']}")

def add_task():
    task = input("Enter new task: ")
    tasks.append({"task": task, "completed": False})
    save_to_file("tasks.json", tasks)
    print("Task added successfully!")

def edit_task():
    display_tasks()
    if not tasks:
        return
    try:
        task_number = int(input("Enter task number to edit: "))
        new_task = input("Enter new task: ")
        tasks[task_number - 1]["task"] = new_task
        save_to_file("tasks.json", tasks)
        print("Task updated!")
    except (ValueError, IndexError):
        print("Invalid input!")

def delete_task():
    display_tasks()
    if not tasks:
        return
    try:
        task_number = int(input("Enter task number to delete: "))
        tasks.pop(task_number - 1)
        save_to_file("tasks.json", tasks)
        print("Task deleted!")
    except (ValueError, IndexError):
        print("Invalid input!")

def display_tasks():
    for i, task in enumerate(tasks, 1):
        emoji = "✅" if task["completed"] else "❌"
        print(f"{i}. {task['task']} {emoji}")

def search_tasks():
    search = input("Enter search term: ")
    results = [task for task in tasks if search.lower() in task["task"].lower()]
    if results:
        for i, task in enumerate(results, 1):
            emoji = "✅" if task["completed"] else "❌"
            print(f"{i}. {task['task']} {emoji}")
    else:
        print("No matching tasks found.")

while True:
    print("\nUser Menu:")
    print("1. Add task")
    print("2. Edit task")
    print("3. Delete task")
    print("4. View tasks")
    print("5. Search tasks")
    print("6. Mark task as done")
    print("7. Login as admin")
    print("8. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        edit_task()
    elif choice == "3":
        delete_task()
    elif choice == "4":
        display_tasks()
    elif choice == "5":
        search_tasks()
    elif choice == "6":
        display_tasks()
        if len(tasks) > 0:
            task_num = int(input("Enter task number to mark as done: "))
            if task_num <= len(tasks):
                tasks[task_num-1]["completed"] = True
                print("Task marked as done!")
            else:
                print("Invalid task number!")
    elif choice == "7":
        current_user = login()
        if current_user and current_user["role"] == "admin":
            while True:
                print("\nAdmin Menu:")
                print("1. Add user")
                print("2. Delete user")
                print("3. View users")
                print("4. Add task")
                print("5. Edit task")
                print("6. Delete task")
                print("7. View tasks")
                print("8. Logout")

                admin_choice = input("Choose an option: ")

                if admin_choice == "1":
                    add_user()
                elif admin_choice == "2":
                    delete_user()
                elif admin_choice == "3":
                    view_users()
                elif admin_choice == "4":
                    add_task()
                elif admin_choice == "5":
                    edit_task()
                elif admin_choice == "6":
                    delete_task()
                elif admin_choice == "7":
                    display_tasks()
                elif admin_choice == "8":
                    print("Logged out from admin mode.")
                    break
                else:
                    print("Invalid choice! Please try again.")
        else:
            print("Access denied! Admin login required.")
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid choice! Please try again.")