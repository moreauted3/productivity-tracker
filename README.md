<h1> Productivity Tracker </h1>

A simple command-line to-do list tracker that saves tasks to a CSV file per user, so your task history persists between sessions.

<h2>System Requirements</h2>

- Windows OS
- Python 3 installed and added to your system PATH
- No external libraries required — uses only the Python standard library (`csv`, `os`, `datetime`)

<h2> Getting Started </h2>

1. Download or clone this repository
2. Double-click `run.bat` to launch the program
3. Enter a username when prompted — this determines which CSV file your tasks are saved to and loaded from

<h2> Features </h2>

- **Per-user task storage** — each username gets its own CSV file (`{username}_tasks.csv`), so multiple people can use the tool without overwriting each other's data
- **Homepage on launch** — automatically checks whether you've logged any tasks today:
  - If you have, offers to view today's tasks or add a new one
  - If you haven't, offers to view your 5 most recent tasks or add a new one
- **Add new tasks** — records the task description, creation date, and an initial status of "Untouched"
- **Edit task status** — update a task's status to Untouched, In progress, Aborted, or Finished
- **Delete individual tasks** — select and remove a single task
- **Delete tasks by date** — remove all tasks logged on a specific date, with a preview and confirmation before anything is deleted
- **Date input validation** — entering an invalid date format returns a clear error message rather than failing silently
- **Double-click launch** — `run.bat` opens a terminal and runs the program automatically, no command-line experience needed

<h2> Planned Features </h2>

- Task priority levels
- Sorting/filtering by status
- macOS/Linux launcher support