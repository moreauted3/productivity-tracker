## take tasks for day
##
from datetime import date
user_tasks =[]
possible_statuses = ("Untouched","In progress", "Aborted","Finished")

class user_errand:
    def __init__(self, task, date_of_creation, status):
        self.task = task
        self.date_of_creation = date_of_creation
        self.status = status

def take_task():
    new_task = str(input("State new item for to-do list:"))
    new_date= date.today()
    new_status = possible_statuses[0]
    errand = user_errand(new_task, new_date, new_status)
    print(errand.task)
    return errand

take_task()



