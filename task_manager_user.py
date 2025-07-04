"""
Task manager user module.
Main task management functions for regular users.
"""

from loads import load_tasks
from saves import save_tasks
from statistics_user import user_statistics_menu
from search_filter import search_and_filter_menu
from screen_utils import clear_screen, display_last_action, display_full_screen_menu
from colors import Colors, success, error, warning, info, title, border, prompt
from task_utils import (
    list_unfinished_tasks_for_user,
    list_pending_tasks_sorted_by_user,
    display_task_list,
    get_completed_tasks,
    get_user_tasks
)


def add_task(username):
    """
    Add a new task for the given user with input validation.

    Args:
        username (str): The username to add the task for.
    """
    print(title("\n--- Add New Task ---"))

    # Title validation (required)
    while True:
        title_input = input(prompt("Title (required): ")).strip()
        if title_input:
            break
        print(error("Error: Title is required. Please enter a title."))

    # Description (optional)
    description = input(prompt("Description (optional): ")).strip()

    # Priority validation (required: 1, 2, or 3)
    while True:
        priority = input(prompt("Priority (1=High, 2=Medium, 3=Low): ")).strip()
        if priority in ["1", "2", "3"]:
            break
        print(error("Error: Priority must be 1, 2, or 3. Please try again."))

    # Deadline validation (required)
    while True:
        deadline = input(prompt("Deadline (YYYY-MM-DD, required): ")).strip()
        if deadline:
            # Basic format validation
            if len(deadline) == 10 and deadline[4] == '-' and deadline[7] == '-':
                try:
                    year, month, day = deadline.split('-')
                    if (len(year) == 4 and year.isdigit() and
                        len(month) == 2 and month.isdigit() and 1 <= int(month) <= 12 and
                        len(day) == 2 and day.isdigit() and 1 <= int(day) <= 31):
                        break
                except ValueError:
                    pass
            print(error("Error: Deadline must be in YYYY-MM-DD format (e.g., 2025-12-31)."))
        else:
            print(error("Error: Deadline is required. Please enter a deadline."))

    # Category validation (required)
    while True:
        category = input(prompt("Category (required): ")).strip()
        if category:
            break
        print(error("Error: Category is required. Please enter a category."))

    task = {
        "title": title_input,
        "description": description,
        "priority": priority,
        "deadline": deadline,
        "category": category,
        "completed": False
    }
    tasks = load_tasks(username)
    tasks.append(task)
    save_tasks(username, tasks)
    print(success("Task added successfully!"))

def list_tasks(username, show_all=False):
    """
    List all tasks for the user. If show_all is False, only pending tasks are shown.

    Args:
        username (str): The username whose tasks to list.
        show_all (bool): Whether to show all tasks or only pending ones.
    """
    tasks = get_user_tasks(username)

    if not show_all:
        tasks = [task for task in tasks if not task.get("completed", False)]

    # Use task_utils function to display task list
    display_task_list(tasks, "Task List", include_user=False)

    # Add pause after displaying tasks unless this is being called from another function
    # The caller will handle the input prompt if needed
    if show_all:  # Only add pause when showing all tasks directly from menu
        print(f"\n{Colors.CYAN}Press Enter to continue...")
        input()

def edit_task(username):
    """
    Edit an existing task for the user.

    Args:
        username (str): The username whose task to edit.
    """
    tasks = load_tasks(username)
    list_tasks(username, show_all=True)

    if not tasks:
        print(warning("No tasks available to edit."))
        return

    try:
        idx = int(input(prompt("Enter the task number to edit: "))) - 1
        if 0 <= idx < len(tasks):
            print(info("Leave blank to keep current value."))
            current_title = tasks[idx]['title']
            current_desc = tasks[idx]['description']
            current_priority = tasks[idx]['priority']
            current_deadline = tasks[idx]['deadline']
            current_category = tasks[idx]['category']

            task_title = (input(f"New title [{Colors.CYAN}{current_title}]: ").strip()
                         or current_title)
            description = (input(f"New description [{Colors.CYAN}{current_desc}]: ").strip()
                          or current_desc)
            priority = (input(f"New priority [{Colors.CYAN}{current_priority}]: ").strip()
                       or current_priority)
            deadline = (input(f"New deadline [{Colors.CYAN}{current_deadline}]: ").strip()
                       or current_deadline)
            category = (input(f"New category [{Colors.CYAN}{current_category}]: ").strip()
                       or current_category)
            tasks[idx].update({
                "title": task_title,
                "description": description,
                "priority": priority,
                "deadline": deadline,
                "category": category
            })
            save_tasks(username, tasks)
            print(success("Task updated successfully!"))
        else:
            print(error("Invalid task number."))
    except (ValueError, IndexError):
        print(error("Invalid input. Please enter a valid task number."))

def remove_task(username):
    """
    Remove a task for the user.

    Args:
        username (str): The username whose task to remove.
    """
    tasks = load_tasks(username)
    list_tasks(username, show_all=True)

    if not tasks:
        print(warning("No tasks available to remove."))
        return

    try:
        idx = int(input(prompt("Enter the task number to remove: "))) - 1
        if 0 <= idx < len(tasks):
            task_title = tasks[idx]['title']
            tasks.pop(idx)
            save_tasks(username, tasks)
            print(success(f"Task '{task_title}' removed successfully!"))
        else:
            print(error("Invalid task number."))
    except (ValueError, IndexError):
        print(error("Invalid input. Please enter a valid task number."))

def mark_task_done(username):
    """
    Mark a task as completed for the user.

    Args:
        username (str): The username whose task to mark as completed.
    """
    tasks = load_tasks(username)
    list_tasks(username)

    if not tasks:
        print(warning("No tasks available to mark as done."))
        return

    while True:
        try:
            user_input = input(prompt("Enter the task number to mark as done (or 'q' to quit): "))

            # Allow user to quit
            if user_input.lower() in ['q', 'quit', 'exit']:
                print(info("Operation cancelled."))
                return

            # Validate input is a number
            if not user_input.isdigit():
                print(error("Error: Please enter a valid number or 'q' to quit."))
                continue

            idx = int(user_input) - 1

            # Check if number is within valid range
            if 0 <= idx < len(tasks):
                # Check if task is already completed
                if tasks[idx].get("completed", False):
                    print(warning(f"Task '{tasks[idx]['title']}' is already completed!"))
                    retry = input(prompt("Try another task? (y/n): ")).strip().lower()
                    if retry != 'y':
                        return
                    continue

                # Mark task as completed
                tasks[idx]["completed"] = True
                save_tasks(username, tasks)
                print(success(f"Task '{tasks[idx]['title']}' marked as completed!"))
                return
            else:
                print(error(f"Error: Please enter a number between 1 and {len(tasks)} "
                           f"or 'q' to quit."))

        except ValueError:
            print(error("Error: Invalid input. Please enter a valid number or 'q' to quit."))
        except (KeyError, IndexError) as e:
            print(error(f"An error occurred: {e}"))
            return

def task_menu(username):
    """
    Main menu for task management for the given user.

    Args:
        username (str): The username for whom to manage tasks.
    """
    last_action = None
    last_result = None

    # Welcome message for user on first entry
    clear_screen()
    print(border("=" * 50))
    print(title(f"        Welcome, {username}!"))
    print(border("=" * 50))
    print(info("You can manage your personal tasks here."))
    print(info("Add, edit, complete, and organize your tasks."))

    while True:
        menu_items = [
            f"{Colors.GREEN}1. {Colors.WHITE}Add new task",
            f"{Colors.BLUE}2. {Colors.WHITE}Edit a task",
            f"{Colors.RED}3. {Colors.WHITE}Remove a task",
            f"{Colors.YELLOW}4. {Colors.WHITE}List pending tasks",
            f"{Colors.MAGENTA}5. {Colors.WHITE}Mark task as completed",
            f"{Colors.CYAN}6. {Colors.WHITE}View completed tasks",
            f"{Colors.WHITE}7. {Colors.WHITE}List all tasks",
            f"{Colors.RED}8. {Colors.WHITE}View unfinished tasks (overdue)",
            f"{Colors.GREEN}9. {Colors.WHITE}Statistics",
            f"{Colors.BLUE}10. {Colors.WHITE}Search & Filter tasks",
            f"{Colors.RED}0. {Colors.WHITE}Logout"
        ]

        # Display the menu
        display_full_screen_menu(
            menu_items,
            f"Task Management - {username}",
            "Personal Task Management System"
        )

        # Display last action if available
        if last_action and last_result:
            display_last_action(last_action, last_result)

        choice = input(prompt("Choose an option: ")).strip()

        try:
            if choice == "1":
                last_action = success("Add new task")
                add_task(username)
                last_result = success("Task addition process completed")
            elif choice == "2":
                last_action = info("Edit task")
                edit_task(username)
                last_result = success("Task editing process completed")
            elif choice == "3":
                last_action = warning("Remove task")
                remove_task(username)
                last_result = success("Task removal process completed")
            elif choice == "4":
                last_action = info("List pending tasks")
                list_pending_tasks_sorted(username)
                last_result = success("Pending tasks displayed")
            elif choice == "5":
                last_action = info("Mark task as completed")
                mark_task_done(username)
                last_result = success("Task completion process executed")
            elif choice == "6":
                last_action = info("View completed tasks")
                list_completed_tasks(username)
                last_result = success("Completed tasks displayed")
            elif choice == "7":
                last_action = info("List all tasks")
                list_tasks(username, show_all=True)
                last_result = success("All tasks displayed")
            elif choice == "8":
                last_action = info("View unfinished tasks")
                list_unfinished_tasks_for_user(username)
                last_result = success("Unfinished tasks displayed")
                input(f"\n{Colors.CYAN}Press Enter to continue...")
            elif choice == "9":
                last_action = info("View statistics")
                user_statistics_menu(username)
                last_result = success("Statistics menu accessed")
                # No input needed here as statistics menu handles its own pauses
            elif choice == "10":
                last_action = info("Search & filter tasks")
                search_and_filter_menu(username)
                last_result = success("Search & filter menu accessed")
                # No input needed here as search menu handles its own pauses
            elif choice == "0":
                clear_screen()
                print(success("Logging out..."))
                break
            else:
                last_action = error(f"Invalid option: {choice}")
                last_result = error("Please choose a valid option (0-10)")

            # Wait for user before clearing screen (except for logout and submenus)
            if choice not in ["0", "4", "6", "7", "8", "9", "10"]:
                input(f"\n{Colors.CYAN}Press Enter to continue...")

        except (ValueError, KeyError, IndexError) as e:
            last_action = error(f"Error in option {choice}")
            last_result = error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...")

def list_completed_tasks(username):
    """
    List only completed tasks for the user.

    Args:
        username (str): The username whose completed tasks to list.
    """
    tasks = get_user_tasks(username)
    completed_tasks = get_completed_tasks(tasks)

    display_task_list(completed_tasks, "Completed Tasks", include_user=False)

    # Add pause after displaying tasks
    print(f"\n{Colors.CYAN}Press Enter to continue...")
    input()

def list_pending_tasks_sorted(username):
    """
    List pending tasks with sorting options.

    Args:
        username (str): The username whose pending tasks to list.
    """
    # Use the common function from task_utils
    list_pending_tasks_sorted_by_user(username)

    # input is already handled in the task_utils function
