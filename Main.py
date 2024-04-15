import os
import json
import datetime
import subprocess

DATA_FILE = "library_data.json"

library_data = {
    "users": {
        "DemoAdmin": {
            "password": "adminpassword",
            "admin": True,
            "banned": False,
            "suspended": False,
            "suspension_date": None,
            "fine": 0,
            "books_checked_out": []
        },
        "DemoUser": {
            "password": "userpassword",
            "admin": False,
            "banned": False,
            "suspended": False,
            "suspension_date": None,
            "fine": 0,
            "books_checked_out": []
        }
    },
    "books": {}
}

def clear_console():
    subprocess.call("clear" if os.name == "posix" else "cls", shell=True)

def load_data():
    global library_data
    try:
        with open(DATA_FILE, "r") as file:
            library_data = json.load(file)
    except FileNotFoundError:
        print("Library data file not found. Starting with empty data.")
    except json.JSONDecodeError as e:
        print("Error decoding JSON data in library data file.")
        print(f"Error message: {e.msg}")
        print(f"Line: {e.lineno}, Column: {e.colno}")
        print(f"Position: {e.pos}")
        print(f"Character: {e.doc[e.pos]}")
    except PermissionError:
        print("Permission denied. Unable to load library data.")

def save_data():
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(library_data, file, indent=4)
    except PermissionError:
        print("Permission denied. Unable to save library data.")

def show_menu():
    clear_console()
    print("Welcome to the Library!")
    print("Please choose an option:")
    print("1: Login")
    print("2: Save and Exit")
    print("3: Exit")

def login():
    clear_console()
    print("Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in library_data["users"]:
        user = library_data["users"][username]
        if user["password"] == password:
            if user["banned"]:
                print("Sorry, you are banned and cannot log in.")
            elif user["suspended"]:
                suspension_date = user["suspension_date"]
                print(f"Sorry, you are suspended until {suspension_date}.")
            else:
                if user["admin"]:
                    show_admin_menu(username)
                else:
                    show_user_menu(username)
        else:
            print("Invalid password!")
            input("Press Enter to continue...")
            show_menu()
    else:
        print("Invalid username!")
        input("Press Enter to continue...")
        show_menu()

def show_admin_menu(username):
    clear_console()
    print(f"Hello, {username} (Admin)!")
    print("Please choose an option:")
    print("1: Add Fine")
    print("2: Remove Fine")
    print("3: Ban User")
    print("4: Remove Ban")
    print("5: Suspend User")
    print("6: Add Book")
    print("7: Logout")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_fine()
    elif choice == "2":
        remove_fine()
    elif choice == "3":
        ban_user()
    elif choice == "4":
        remove_ban()
    elif choice == "5":
        suspend_user()
    elif choice == "6":
        add_book()
    elif choice == "7":
        save_data()
        show_menu()
    else:
        print("Invalid choice!")
        input("Press Enter to continue...")
        show_admin_menu(username)

def show_user_menu(username):
    clear_console()
    print(f"Hello, {username}!")
    print("Please choose an option:")
    print("1: Check Out Book")
    print("2: Return Book")
    print("3: Logout")

    choice = input("Enter your choice: ")

    if choice == "1":
        check_out_book(username)
    elif choice == "2":
        return_book(username)
    elif choice == "3":
        show_menu()
    else:
        print("Invalid choice!")
        input("Press Enter to continue...")
        show_user_menu(username)

def check_out_book(username):
    if "books" not in library_data:
        library_data["books"] = {}

    book_name = input("Enter the book name: ")
    if book_name in library_data["books"]:
        book = library_data["books"][book_name]
        if book["checked_out"]:
            print("Sorry, the book is already checked out.")
        else:
            user = library_data["users"][username]
            user["books_checked_out"].append(book_name)
            book["checked_out"] = True
            book["checked_out_by"] = username
            print(f"Book '{book_name}' checked out successfully by {username}.")
    else:
        print("Invalid book name!")

    input("Press Enter to continue...")
    show_user_menu(username)

def return_book(username):
    user = library_data["users"][username]
    books_checked_out = user["books_checked_out"]
    if len(books_checked_out) == 0:
        print("You haven't checked out any books.")
    else:
        print("Books checked out by you:")
        for i, book_name in enumerate(books_checked_out):
            print(f"{i+1}: {book_name}")

        choice = input("Enter the number of the book you want to return (or '0' to cancel): ")
        if choice == "0":
            return

        try:
            choice = int(choice)
            if 1 <= choice <= len(books_checked_out):
                book_name = books_checked_out[choice - 1]
                book = library_data["books"][book_name]
                book["checked_out"] = False
                book["checked_out_by"] = None
                user["books_checked_out"].remove(book_name)
                print(f"Book '{book_name}' returned successfully.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid choice!")

    input("Press Enter to continue...")
    show_user_menu(username)

def add_book():
    book_name = input("Enter the book name: ")
    book_author = input("Enter the book author: ")

    if book_name in library_data["books"]:
        print("Book already exists!")
    else:
        library_data["books"][book_name] = {
            "author": book_author,
            "checked_out": False,
            "checked_out_by": None
        }
        print(f"Book '{book_name}' by {book_author} added successfully.")

    input("Press Enter to continue...")
    show_admin_menu("Admin")

def add_fine():
    username = input("Enter the username: ")
    amount = input("Enter the fine amount: ")
    if username in library_data["users"]:
        user = library_data["users"][username]
        user["fine"] += float(amount)
        print(f"Fine of {amount} added to {username}.")
    else:
        print("Invalid username!")

    input("Press Enter to continue...")
    show_admin_menu("Admin")

def remove_fine():
    username = input("Enter the username: ")
    amount = input("Enter the fine amount to remove: ")
    if username in library_data["users"]:
        user = library_data["users"][username]
        if user["fine"] >= float(amount):
            user["fine"] -= float(amount)
            print(f"{amount} removed from the fine of {username}.")
        else:
            print(f"The fine of {username} is less than {amount}.")
    else:
        print("Invalid username!")

    input("Press Enter to continue...")
    show_admin_menu("Admin")

def ban_user():
    username = input("Enter the username to ban: ")
    if username in library_data["users"]:
        user = library_data["users"][username]
        user["banned"] = True
        print(f"{username} is now banned.")
    else:
        print("Invalid username!")

    input("Press Enter to continue...")
    show_admin_menu("Admin")

def remove_ban():
    username = input("Enter the username to remove the ban: ")
    if username in library_data["users"]:
        user = library_data["users"][username]
        user["banned"] = False
        print(f"{username} is no longer banned.")
    else:
        print("Invalid username!")

    input("Press Enter to continue...")
    show_admin_menu("Admin")

def suspend_user():
    username = input("Enter the username to suspend: ")
    suspension_date = input("Enter the suspension end date (YYYY-MM-DD): ")

    if username in library_data["users"]:
        user = library_data["users"][username]
        user["suspended"] = True
        user["suspension_date"] = suspension_date
        print(f"{username} is now suspended until {suspension_date}.")
    else:
        print("Invalid username!")

    input("Press Enter to continue...")
    show_admin_menu("Admin")

def main():
    load_data()

    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            login()
        elif choice == "2":
            save_data()
            print("Library data saved. Exiting...")
            break
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
