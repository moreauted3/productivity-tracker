import csv
import os
from datetime import date
import pandas as pd

## INITIALISES ALL FUNCTIONS, IMPORTANT DATA

possible_statuses = ("Untouched", "In progress", "Aborted", "Finished")

class user_errand:
    def __init__(self, task, date_of_creation, status, index):
        self.task = task
        self.date_of_creation = date_of_creation
        self.status = status
        self.index = index  

    def to_row(self):
        return [self.task, self.date_of_creation, self.status]


def get_user_csv_path(username):
    return f"{username}_tasks.csv"

##

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
    errand = user_errand(new_task, new_date, new_status)
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


def get_todays_tasks(tasks):
    ## looks through user's csv and creates a list of any errands with today's date
    today_str = str(date.today())
    return [t for t in tasks if t["date_of_creation"] == today_str]


def display_tasks(tasks):
    if not tasks:
        print("No tasks to show.")
        return
    for t in tasks:
        print(f"- {t['task']} | {t['date_of_creation']} | {t['status']}")
        edit_yesno = input("Would you like to edit any of these tasks?")
        if edit_yesno == "yes":
            pass ## which task would you like to edit, then pass to edit_task()

def delete_task(task):
     usercsv =get_user_csv_path(username)
     df = pd.read_csv(f"{usercsv}.csv")
     df.drop(task)



def edit_task(task):
    action = str(input("Would you like to delete (d), edit status (es) or edit date tbd (ed)?"))
    if action == "d":
        pass
    elif action == "es":
        pass
    elif action == "ed":
        pass
def homepage(username):
    tasks = load_tasks(username)
    todays_tasks = get_todays_tasks(tasks)

    if todays_tasks:
        choice = input("You have tasks logged today. View them (v) or add a new one (n)? ").strip().lower()
        if choice == "v":
            display_tasks(todays_tasks)
        elif choice == "n":
            take_task(username)
    else:
        choice = input("No tasks today yet. Add a new one (n) or view your last 5 tasks (v)? ").strip().lower()
        if choice == "n":
            take_task(username)
        elif choice == "v":
            display_tasks(tasks[-5:])

## ACTUAL INTERFACE

if __name__ == "__main__":
    username = input("Enter your username: ")
    homepage(username)