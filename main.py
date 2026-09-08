import csv
import os
from datetime import date

possible_statuses = ("Untouched", "In progress", "Aborted", "Finished")

class user_errand:
    def __init__(self, task, date_of_creation, status, task_id= None):
        self.task = task
        self.date_of_creation = date_of_creation
        self.status = status
        self.task_id = task_id

    def to_row(self):
        return [self.task, self.date_of_creation, self.status, self.task_id]


def get_user_csv_path(username):
    return f"{username}_tasks.csv"


def save_task(errand, username):
    filepath = get_user_csv_path(username)
    file_exists = os.path.isfile(filepath)
    with open(filepath, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["task", "date_of_creation", "status"])  # header, written once
        writer.writerow(errand.to_row())


def take_task(username):
    new_task = str(input("State new item for to-do list:"))
    new_date = date.today()
    new_status = possible_statuses[0]
    new_id = get_next_id(username)
    errand = user_errand(new_task, new_date, new_status, task_id=new_id)
    save_task(errand, username)
    print(f"Saved: {errand.task}")
    return errand

def load_tasks(username):
    filepath = get_user_csv_path(username)
    if not os.path.isfile(filepath):
        return []
    with open(filepath, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_next_id(username):
    tasks = load_tasks(username)
    if not tasks:
        return 1
    return max(int(t["id"]) for t in tasks) + 1

def save_task(errand, username):
    filepath = get_user_csv_path(username)
    file_exists = os.path.isfile(filepath)
    with open(filepath, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["id", "task", "date_of_creation", "status"])
        writer.writerow([errand.task_id, errand.task, errand.date_of_creation, errand.status])

def get_todays_tasks(tasks):
    today_str = str(date.today())
    return [t for t in tasks if t["date_of_creation"] == today_str]


def display_tasks(tasks):
    if not tasks:
        print("No tasks to show.")
        return
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. [{t['status']}] {t['task']} ({t['date_of_creation']})")


def select_task(tasks): ## should be used when stating variable value
    display_tasks(tasks)
    choice = input("Enter the number of the task to edit (or 0 to cancel): ").strip()
    if choice == "0" or not choice.isdigit() or not (1 <= int(choice) <= len(tasks)):
        return None
    return tasks[int(choice) - 1]  # dict with 'id', 'task', 'date_of_creation', 'status'


def update_task_status(username, selected_task):
    all_tasks = load_tasks(username)
    for t in all_tasks:
        if t["id"] == selected_task["id"]:
            for i, status in enumerate(possible_statuses, start=1):
                print(f"{i}. {status}")
            choice = input("New status number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(possible_statuses):
                t["status"] = possible_statuses[int(choice) - 1]
                rewrite_csv(username, all_tasks)
                print("Updated.")
            else:
                print("Invalid choice, cancelled.")
            return
    print("Task not found — it may have been removed since you last viewed it.")


def rewrite_csv(username, tasks):
    filepath = get_user_csv_path(username)
    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "task", "date_of_creation", "status"])
        writer.writeheader()
        writer.writerows(tasks)

def return_to_homepage():
    ask = str(input("Would you like to return to homepage? (y)es or (n)o"))
    if ask =="y":
        homepage(username)
    else:
        pass

def handle_task_action(username, tasks):
    if not tasks:
        return

    action = input("Would you like to (e)dit a task's status, (d)elete a task, or (b)ack? ").strip().lower()

    if action == "e":
        selected = select_task(tasks)
        if selected:
            update_task_status(username, selected)
            return_to_homepage()

    elif action == "d":
        selected = select_task(tasks)
        if selected:
            delete_task(username, selected)
            return_to_homepage()
            

    elif action == "b":
        return

    else:
        print("Invalid choice.")
    
def homepage(username):
    tasks = load_tasks(username)
    todays_tasks = get_todays_tasks(tasks)

    if todays_tasks:
        choice = input("You have tasks logged today. View them (v) or add a new one (n)? ").strip().lower()

        if choice == "v":
            display_tasks(todays_tasks)
            handle_task_action(username, todays_tasks)

        elif choice == "n":
            take_task(username)

    else:
        choice = input("No tasks today yet. Add a new one (n) or view your last 5 tasks (v)? ").strip().lower()

        if choice == "n":
            take_task(username)

        elif choice == "v":
            recent_tasks = tasks[-5:]
            display_tasks(recent_tasks)
            handle_task_action(username, recent_tasks)

def delete_task(username, selected_task):
    all_tasks = load_tasks(username)
    remaining = [t for t in all_tasks if t["id"] != selected_task["id"]]
    if len(remaining) == len(all_tasks):
        print("Task not found — it may have been removed since you last viewed it.")
        return
    rewrite_csv(username, remaining)
    print("Deleted.")


def delete_tasks_by_date(username, target_date_str):
    all_tasks = load_tasks(username)
    to_delete = [t for t in all_tasks if t["date_of_creation"] == target_date_str]

    if not to_delete:
        print(f"No tasks found for {target_date_str}.")
        return

    display_tasks(to_delete)
    confirm = input(f"Delete these {len(to_delete)} task(s)? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    remaining = [t for t in all_tasks if t["date_of_creation"] != target_date_str]
    rewrite_csv(username, remaining)
    print(f"Deleted {len(to_delete)} task(s).")


def delete_task(username, selected_task):
    all_tasks = load_tasks(username)
    remaining = [t for t in all_tasks if t["id"] != selected_task["id"]]
    if len(remaining) == len(all_tasks):
        print("Task not found — it may have been removed since you last viewed it.")
        return
    rewrite_csv(username, remaining)
    print("Deleted.")


def delete_tasks_by_date(username, target_date_str):
    all_tasks = load_tasks(username)
    to_delete = [t for t in all_tasks if t["date_of_creation"] == target_date_str]

    if not to_delete:
        print(f"No tasks found for {target_date_str}.")
        return

    display_tasks(to_delete)
    confirm = input(f"Delete these {len(to_delete)} task(s)? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    remaining = [t for t in all_tasks if t["date_of_creation"] != target_date_str]
    rewrite_csv(username, remaining)
    print(f"Deleted {len(to_delete)} task(s).")


def delete_by_date_flow(username):
    target_date_str = input("Enter date to delete tasks from (YYYY-MM-DD): ").strip()
    delete_tasks_by_date(username, target_date_str)

if __name__ == "__main__":
    username = input("Enter your username: ")
    homepage(username)