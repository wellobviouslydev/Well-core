
import os
import sys
import json
import platform
from pathlib import Path
from datetime import datetime


# ==============================================
# WELL CORE
# Personal System Console
# Version: 1.0.0
# ==============================================

APP_NAME = "WELL CORE"
VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "well_data.json"

RED = "\033[91m"
DARK_RED = "\033[31m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RESET = "\033[0m"


# ==============================================
# DATA MANAGEMENT
# ==============================================

def initialize():

    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        save_data({
            "tasks": [],
            "notes": []
        })


def load_data():

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("tasks", [])
        data.setdefault("notes", [])

        return data

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "tasks": [],
            "notes": []
        }


def save_data(data):

    DATA_DIR.mkdir(exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# ==============================================
# INTERFACE
# ==============================================

def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")


def pause():

    input(f"\n{GRAY}Press ENTER to continue...{RESET}")


def header():

    clear_screen()

    print(RED + r"""
 __        __ ______ _      _       _____ ____  _____  _____
 \ \      / /|  ____| |    | |     / ____/ __ \|  __ \|  __ \
  \ \ /\ / / | |__  | |    | |    | |   | |  | | |__) | |__) |
   \ V  V /  |  __| | |    | |    | |   | |  | |  _  /|  ___/
    \_/\_/   | |____| |____| |____| |___| |__| | | \ \| |
             |______|______|______|\_____\____/|_|  \_\_|
""" + RESET)

    print(f"{WHITE}{APP_NAME} | VERSION {VERSION}{RESET}")
    print(f"{GRAY}{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}{RESET}")

    print(RED + "=" * 58 + RESET)


# ==============================================
# SYSTEM INFORMATION
# ==============================================

def system_information():

    header()

    print(f"\n{RED}[ SYSTEM INFORMATION ]{RESET}\n")

    print(f"Operating System : {platform.system()}")
    print(f"OS Version       : {platform.version()}")
    print(f"Architecture     : {platform.machine()}")
    print(f"Processor        : {platform.processor()}")
    print(f"Python Version   : {platform.python_version()}")

    pause()


# ==============================================
# TASK MANAGEMENT
# ==============================================

def show_tasks():

    header()

    data = load_data()

    print(f"\n{RED}[ TASK MANAGER ]{RESET}\n")

    if not data["tasks"]:
        print("No tasks available.")

    else:

        for index, task in enumerate(data["tasks"], start=1):

            status = "DONE" if task["completed"] else "PENDING"

            print(f"{index}. [{status}] {task['title']}")

    pause()


def add_task():

    header()

    data = load_data()

    print(f"\n{RED}[ ADD NEW TASK ]{RESET}\n")

    title = input("Task title: ").strip()

    if not title:

        print("Task cannot be empty.")
        pause()
        return

    data["tasks"].append({
        "title": title,
        "completed": False,
        "created_at": datetime.now().isoformat()
    })

    save_data(data)

    print("\nTask successfully added.")

    pause()


def complete_task():

    header()

    data = load_data()

    print(f"\n{RED}[ COMPLETE TASK ]{RESET}\n")

    if not data["tasks"]:

        print("No tasks available.")
        pause()
        return

    for index, task in enumerate(data["tasks"], start=1):

        status = "DONE" if task["completed"] else "PENDING"

        print(f"{index}. [{status}] {task['title']}")

    try:

        choice = int(input("\nTask number: "))

        if 1 <= choice <= len(data["tasks"]):

            data["tasks"][choice - 1]["completed"] = True

            save_data(data)

            print("Task completed successfully.")

        else:

            print("Invalid task number.")

    except ValueError:

        print("Please enter a valid number.")

    pause()


# ==============================================
# NOTES MANAGER
# ==============================================

def notes_manager():

    header()

    data = load_data()

    print(f"\n{RED}[ NOTES MANAGER ]{RESET}\n")

    print("1. View notes")
    print("2. Add note")
    print("3. Return")

    choice = input("\nSelect: ").strip()

    if choice == "1":

        header()

        if not data["notes"]:

            print("No notes available.")

        else:

            for index, note in enumerate(data["notes"], start=1):

                print(f"{index}. {note['content']}")

        pause()

    elif choice == "2":

        content = input("\nWrite your note: ").strip()

        if content:

            data["notes"].append({
                "content": content,
                "created_at": datetime.now().isoformat()
            })

            save_data(data)

            print("Note saved.")

        else:

            print("Note cannot be empty.")

        pause()


# ==============================================
# DASHBOARD
# ==============================================

def dashboard():

    data = load_data()

    total = len(data["tasks"])

    completed = sum(
        1 for task in data["tasks"]
        if task["completed"]
    )

    print(f"\n{RED}[ DASHBOARD ]{RESET}\n")

    print(f"Total Tasks     : {total}")
    print(f"Completed Tasks : {completed}")
    print(f"Pending Tasks   : {total - completed}")
    print(f"Total Notes     : {len(data['notes'])}")


# ==============================================
# MAIN APPLICATION
# ==============================================

def main():

    initialize()

    while True:

        header()

        dashboard()

        print(f"\n{RED}[ MAIN MENU ]{RESET}\n")

        print("1. System Information")
        print("2. View Tasks")
        print("3. Add Task")
        print("4. Complete Task")
        print("5. Notes Manager")
        print("0. Exit")

        choice = input(f"\n{RED}WELL >> {RESET}").strip()

        if choice == "1":

            system_information()

        elif choice == "2":

            show_tasks()

        elif choice == "3":

            add_task()

        elif choice == "4":

            complete_task()

        elif choice == "5":

            notes_manager()

        elif choice == "0":

            clear_screen()

            print(f"\n{RED}WELL CORE SHUTTING DOWN...{RESET}")

            print("Session terminated.")

            sys.exit(0)

        else:

            print("\nInvalid selection.")

            pause()


# ==============================================
# APPLICATION ENTRY POINT
# ==============================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n\nWELL CORE interrupted.")

        sys.exit(0)
