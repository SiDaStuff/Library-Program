import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime, timedelta

# Load data from JSON file
def load_data():
    try:
        with open('lb.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"books": [], "users": {}}

# Save data to JSON file
def save_data(data):
    with open('lb.json', 'w') as f:
        json.dump(data, f, indent=4)

data = load_data()

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username in data["users"] and data["users"][username]["password"] == password:
        status = data["users"][username]["status"]
        if status == "Admin":
            admin_menu(username)
        else:
            user_menu(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to create admin menu
def admin_menu(username):
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Menu")
    admin_window.geometry("400x400")

    def open_manage_books():
        manage_books_window = tk.Toplevel(admin_window)
        manage_books_window.title("Manage Books")
        manage_books_window.geometry("400x400")

        def add_book():
            add_book_window = tk.Toplevel(manage_books_window)
            add_book_window.title("Add Book")
            add_book_window.geometry("300x200")

            new_book_id = max(book['id'] for book in data["books"]) + 1 if data["books"] else 1
            tk.Label(add_book_window, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
            entry_book_id = tk.Entry(add_book_window)
            entry_book_id.grid(row=0, column=1, padx=10, pady=10)
            entry_book_id.insert(0, new_book_id)

            tk.Label(add_book_window, text="Book Name:").grid(row=1, column=0, padx=10, pady=10)
            entry_book_name = tk.Entry(add_book_window)
            entry_book_name.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(add_book_window, text="Shelf Name:").grid(row=2, column=0, padx=10, pady=10)
            entry_book_shelf = tk.Entry(add_book_window)
            entry_book_shelf.grid(row=2, column=1, padx=10, pady=10)

            def save_book():
                book_id = int(entry_book_id.get())
                book_name = entry_book_name.get()
                book_shelf = entry_book_shelf.get()

                if book_name and book_shelf:
                    new_book = {"id": book_id, "name": book_name, "shelf": book_shelf}
                    data["books"].append(new_book)
                    save_data(data)
                    add_book_window.destroy()
                    manage_books_window.destroy()
                    open_manage_books()
                else:
                    messagebox.showerror("Error", "Invalid input")

            save_button = tk.Button(add_book_window, text="Save", command=save_book, font=("Helvetica", 14), bg="#4CAF50", fg="black")
            save_button.grid(row=3, columnspan=2, pady=10)

        def edit_book(book):
            edit_book_window = tk.Toplevel(manage_books_window)
            edit_book_window.title("Edit Book")
            edit_book_window.geometry("300x200")

            tk.Label(edit_book_window, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
            entry_book_id = tk.Entry(edit_book_window)
            entry_book_id.grid(row=0, column=1, padx=10, pady=10)
            entry_book_id.insert(0, book["id"])

            tk.Label(edit_book_window, text="Book Name:").grid(row=1, column=0, padx=10, pady=10)
            entry_book_name = tk.Entry(edit_book_window)
            entry_book_name.grid(row=1, column=1, padx=10, pady=10)
            entry_book_name.insert(0, book["name"])

            tk.Label(edit_book_window, text="Shelf Name:").grid(row=2, column=0, padx=10, pady=10)
            entry_book_shelf = tk.Entry(edit_book_window)
            entry_book_shelf.grid(row=2, column=1, padx=10, pady=10)
            entry_book_shelf.insert(0, book["shelf"])

            def save_book():
                book["id"] = int(entry_book_id.get())
                book["name"] = entry_book_name.get()
                book["shelf"] = entry_book_shelf.get()

                if book["name"] and book["shelf"]:
                    save_data(data)
                    edit_book_window.destroy()
                    manage_books_window.destroy()
                    open_manage_books()
                else:
                    messagebox.showerror("Error", "Invalid input")

            save_button = tk.Button(edit_book_window, text="Save", command=save_book, font=("Helvetica", 14), bg="#4CAF50", fg="black")
            save_button.grid(row=3, columnspan=2, pady=10)

        def delete_book(book):
            data["books"].remove(book)
            save_data(data)
            manage_books_window.destroy()
            open_manage_books()

        add_book_button = tk.Button(manage_books_window, text="Add Book", command=add_book, font=("Helvetica", 14), bg="#4CAF50", fg="black")
        add_book_button.pack(pady=10)

        for book in data["books"]:
            book_frame = tk.Frame(manage_books_window)
            book_frame.pack(fill="x", padx=5, pady=2)
            book_label = tk.Label(book_frame, text=f"ID: {book['id']}, Name: {book['name']}, Shelf: {book['shelf']}")
            book_label.pack(side="left")
            edit_button = tk.Button(book_frame, text="Edit", command=lambda b=book: edit_book(b), font=("Helvetica", 10), bg="#4CAF50", fg="black")
            edit_button.pack(side="left")
            delete_button = tk.Button(book_frame, text="Delete", command=lambda b=book: delete_book(b), font=("Helvetica", 10), bg="#f44336", fg="black")
            delete_button.pack(side="left")

        close_button = tk.Button(manage_books_window, text="Close", command=manage_books_window.destroy, font=("Helvetica", 14), bg="#f44336", fg="black")
        close_button.pack(pady=10)

    def open_manage_users():
        manage_users_window = tk.Toplevel(admin_window)
        manage_users_window.title("Manage Users")
        manage_users_window.geometry("400x400")

        def edit_user(user_key, user):
            edit_user_window = tk.Toplevel(manage_users_window)
            edit_user_window.title("Edit User")
            edit_user_window.geometry("300x250")

            tk.Label(edit_user_window, text="Password:").grid(row=0, column=0, padx=10, pady=10)
            entry_password = tk.Entry(edit_user_window)
            entry_password.grid(row=0, column=1, padx=10, pady=10)
            entry_password.insert(0, user["password"])

            tk.Label(edit_user_window, text="Status (User/Admin):").grid(row=1, column=0, padx=10, pady=10)
            entry_status = tk.Entry(edit_user_window)
            entry_status.grid(row=1, column=1, padx=10, pady=10)
            entry_status.insert(0, user["status"])

            tk.Label(edit_user_window, text="Ban Duration (days, 0 for permanent):").grid(row=2, column=0, padx=10, pady=10)
            entry_ban_duration = tk.Entry(edit_user_window)
            entry_ban_duration.grid(row=2, column=1, padx=10, pady=10)

            tk.Label(edit_user_window, text="Fines:").grid(row=3, column=0, padx=10, pady=10)
            entry_fines = tk.Entry(edit_user_window)
            entry_fines.grid(row=3, column=1, padx=10, pady=10)
            entry_fines.insert(0, user["fines"])

            def save_user():
                user["password"] = entry_password.get()
                user["status"] = entry_status.get()
                user["fines"] = float(entry_fines.get())

                if entry_ban_duration.get().isdigit():
                    ban_duration = int(entry_ban_duration.get())
                    user["ban_duration"] = ban_duration

                save_data(data)
                edit_user_window.destroy()
                manage_users_window.destroy()
                open_manage_users()

            save_button = tk.Button(edit_user_window, text="Save", command=save_user, font=("Helvetica", 14), bg="#4CAF50", fg="black")
            save_button.grid(row=4, columnspan=2, pady=10)

        for username, user in data["users"].items():
            user_frame = tk.Frame(manage_users_window)
            user_frame.pack(fill="x", padx=5, pady=2)
            user_label = tk.Label(user_frame, text=f"Username: {username}, Status: {user['status']}")
            user_label.pack(side="left")
            edit_button = tk.Button(user_frame, text="Edit", command=lambda u_key=username, u=user: edit_user(u_key, u), font=("Helvetica", 10), bg="#4CAF50", fg="black")
            edit_button.pack(side="left")

        close_button = tk.Button(manage_users_window, text="Close", command=manage_users_window.destroy, font=("Helvetica", 14), bg="#f44336", fg="black")
        close_button.pack(pady=10)

    def check_out_book():
        book_id = simpledialog.askinteger("Input", "Enter book ID to check out:")
        if book_id:
            for book in data["books"]:
                if book["id"] == book_id:
                    user = data["users"][username]
                    if user["fines"] > 0:
                        messagebox.showerror("Error", "You have outstanding fines and cannot check out books.")
                    else:
                        user["checked_out_books"].append({"id": book_id, "due_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")})
                        save_data(data)
                        messagebox.showinfo("Success", f"Book '{book['name']}' checked out successfully. Due in two weeks.")
                    return
            messagebox.showerror("Error", "Book ID not found")

    def view_checked_out_books():
        checked_out_books_window = tk.Toplevel(admin_window)
        checked_out_books_window.title("Checked Out Books")
        checked_out_books_window.geometry("400x400")

        if data["users"][username]["status"] == "Admin":
            for user_key, user in data["users"].items():
                for book in user["checked_out_books"]:
                    book_info = next((b for b in data["books"] if b["id"] == book["id"]), None)
                    book_name = book_info['name'] if book_info else 'Unknown'
                    book_label = tk.Label(checked_out_books_window, text=f"User: {user_key}, Book ID: {book['id']}, Name: {book_name}, Due Date: {book['due_date']}")
                    book_label.pack()
        else:
            for book in data["users"][username]["checked_out_books"]:
                book_info = next((b for b in data["books"] if b["id"] == book["id"]), None)
                book_name = book_info['name'] if book_info else 'Unknown'
                book_label = tk.Label(checked_out_books_window, text=f"Book ID: {book['id']}, Name: {book_name}, Due Date: {book['due_date']}")
                book_label.pack()

    def return_book():
        book_id = simpledialog.askinteger("Input", "Enter book ID to return:")
        if book_id:
            for book in data["books"]:
                if book["id"] == book_id:
                    user = data["users"][username]
                    for checked_out_book in user["checked_out_books"]:
                        if checked_out_book["id"] == book_id:
                            user["checked_out_books"].remove(checked_out_book)
                            save_data(data)
                            messagebox.showinfo("Success", f"Book '{book['name']}' returned successfully. Place back on '{book['shelf']}' shelf.")
                            return
            messagebox.showerror("Error", "Book ID not found")

    def log_out():
        admin_window.destroy()

    commands = {
        "Manage Books": open_manage_books,
        "Manage Users": open_manage_users,
        "Check Out Book": check_out_book,
        "View Checked Out Books": view_checked_out_books,
        "Return Book": return_book,
        "Log Out": log_out
    }

    for item in ["Manage Books", "Manage Users", "Check Out Book", "View Checked Out Books", "Return Book", "Log Out"]:
        button = tk.Button(admin_window, text=item, command=commands[item], font=("Helvetica", 14), bg="#4CAF50", fg="black", pady=10)
        button.pack(fill="x", padx=10, pady=5)

# Function to create user menu
def user_menu(username):
    user_window = tk.Toplevel(root)
    user_window.title("User Menu")
    user_window.geometry("400x400")

    def check_out_book():
        book_id = simpledialog.askinteger("Input", "Enter book ID to check out:")
        if book_id:
            for book in data["books"]:
                if book["id"] == book_id:
                    user = data["users"][username]
                    if user["fines"] > 0:
                        messagebox.showerror("Error", "You have outstanding fines and cannot check out books.")
                    else:
                        user["checked_out_books"].append({"id": book_id, "due_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")})
                        save_data(data)
                        messagebox.showinfo("Success", f"Book '{book['name']}' checked out successfully. Due in two weeks.")
                    return
            messagebox.showerror("Error", "Book ID not found")

    def view_checked_out_books():
        checked_out_books_window = tk.Toplevel(user_window)
        checked_out_books_window.title("Checked Out Books")
        checked_out_books_window.geometry("400x400")
        
        for book in data["users"][username]["checked_out_books"]:
            book_info = next((b for b in data["books"] if b["id"] == book["id"]), None)
            book_name = book_info['name'] if book_info else 'Unknown'
            book_label = tk.Label(checked_out_books_window, text=f"Book ID: {book['id']}, Name: {book_name}, Due Date: {book['due_date']}")
            book_label.pack()

    def return_book():
        book_id = simpledialog.askinteger("Input", "Enter book ID to return:")
        if book_id:
            for book in data["books"]:
                if book["id"] == book_id:
                    user = data["users"][username]
                    for checked_out_book in user["checked_out_books"]:
                        if checked_out_book["id"] == book_id:
                            user["checked_out_books"].remove(checked_out_book)
                            save_data(data)
                            messagebox.showinfo("Success", f"Book '{book['name']}' returned successfully. Place back on '{book['shelf']}' shelf.")
                            return
            messagebox.showerror("Error", "Book ID not found")

    def view_fines():
        fines = data["users"][username]["fines"]
        messagebox.showinfo("Fines", f"Your current fines amount to: ${fines:.2f}")

    def log_out():
        user_window.destroy()

    commands = {
        "Check Out Book": check_out_book,
        "View Checked Out Books": view_checked_out_books,
        "Return Book": return_book,
        "View Fines": view_fines,
        "Log Out": log_out
    }

    for item in ["Check Out Book", "View Checked Out Books", "Return Book", "View Fines", "Log Out"]:
        button = tk.Button(user_window, text=item, command=commands[item], font=("Helvetica", 14), bg="#4CAF50", fg="black", pady=10)
        button.pack(fill="x", padx=10, pady=5)

# Create the main window
root = tk.Tk()
root.title("Library System")
root.geometry("300x200")

# Create and place the username label and entry
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

# Create and place the password label and entry
tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

# Create and place the login button
login_button = tk.Button(root, text="Sign In", command=login, font=("Helvetica", 14), bg="#4CAF50", fg="black", pady=10)
login_button.grid(row=2, columnspan=2, pady=10)

# Run the main loop
root.mainloop()
