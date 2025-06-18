from loads import load_tasks
from saves import save_tasks
from statistics import statistics_menu # type: ignore

def add_task(username):
    """
    Add a new task for the given user.

    Args:
        username (str): The username to add the task for.
    """
    print("\n--- Add New Task ---")
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    priority = input("Priority (1=High, 2=Medium, 3=Low): ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()
    category = input("Category: ").strip()
    task = {
        "title": title,
        "description": description,
        "priority": priority,
        "deadline": deadline,
        "category": category,
        "completed": False
    }
    tasks = load_tasks(username)
    tasks.append(task)
    save_tasks(username, tasks)
    print("Task added successfully!")

def list_tasks(username, show_all=False):
    """
    List all tasks for the user. If show_all is False, only pending tasks are shown.

    Args:
        username (str): The username whose tasks to list.
        show_all (bool): Whether to show all tasks or only pending ones.
    """
    print("\n--- Task List ---")
    tasks = load_tasks(username)
    found = False
    for idx, task in enumerate(tasks):
        if show_all or not task.get("completed", False):
            status = "Done" if task.get("completed", False) else "Pending"
            print(f"{idx+1}. {task['title']} | {task['description']} | Priority: {task['priority']} | Deadline: {task['deadline']} | Category: {task['category']} | Status: {status}")
            found = True
    if not found:
        print("No tasks found.")

def edit_task(username):
    """
    Edit an existing task for the user.

    Args:
        username (str): The username whose task to edit.
    """
    tasks = load_tasks(username)
    list_tasks(username, show_all=True)
    idx = int(input("Enter the task number to edit: ")) - 1
    if 0 <= idx < len(tasks):
        print("Leave blank to keep current value.")
        title = input(f"New title [{tasks[idx]['title']}]: ").strip() or tasks[idx]['title']
        description = input(f"New description [{tasks[idx]['description']}]: ").strip() or tasks[idx]['description']
        priority = input(f"New priority [{tasks[idx]['priority']}]: ").strip() or tasks[idx]['priority']
        deadline = input(f"New deadline [{tasks[idx]['deadline']}]: ").strip() or tasks[idx]['deadline']
        category = input(f"New category [{tasks[idx]['category']}]: ").strip() or tasks[idx]['category']
        tasks[idx].update({
            "title": title,
            "description": description,
            "priority": priority,
            "deadline": deadline,
            "category": category
        })
        save_tasks(username, tasks)
        print("Task updated successfully!")
    else:
        print("Invalid task number.")

def remove_task(username):
    """
    Remove a task for the user.

    Args:
        username (str): The username whose task to remove.
    """
    tasks = load_tasks(username)
    list_tasks(username, show_all=True)
    idx = int(input("Enter the task number to remove: ")) - 1
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        save_tasks(username, tasks)
        print("Task removed successfully!")
    else:
        print("Invalid task number.")

def mark_task_done(username):
    """
    Mark a task as completed for the user.

    Args:
        username (str): The username whose task to mark as completed.
    """
    tasks = load_tasks(username)
    list_tasks(username)
    idx = int(input("Enter the task number to mark as done: ")) - 1
    if 0 <= idx < len(tasks):
        tasks[idx]["completed"] = True
        save_tasks(username, tasks)
        print("Task marked as completed!")
    else:
        print("Invalid task number.")

def task_menu(username):
    """
    Main menu for task management for the given user.

    Args:
        username (str): The username for whom to manage tasks.
    """
    while True:
        print("\n--- Task Management Menu ---")
        print("1. Add new task")
        print("2. Edit a task")
        print("3. Remove a task")
        print("4. List pending tasks")
        print("5. Mark task as completed")
        print("6. List all tasks")
        print("7. Estatísticas")
        print("0. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_task(username)
        elif choice == "2":
            edit_task(username)
        elif choice == "3":
            remove_task(username)
        elif choice == "4":
            list_tasks(username)
        elif choice == "5":
            mark_task_done(username)
        elif choice == "6":
            list_tasks(username, show_all=True)
        elif choice == "7":
            statistics_menu()
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")