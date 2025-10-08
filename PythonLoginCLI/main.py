import csv
import os
import sys
import time
import msvcrt

DB_FILE = "users.csv"

# ---------------- DB SETUP ----------------
def ensure_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password"])

# ---------------- PASSWORD INPUT ----------------
def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print()
            break
        elif ch == b'\x08':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            password += ch.decode('utf-8', errors='ignore')
            print("*", end="", flush=True)
    return password

# ---------------- DELETE LINES ----------------
def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\r')
    sys.stdout.write('\x1b[2K')
    sys.stdout.flush()

def buffer_and_delete_line():
    for _ in range(3):
        time.sleep(0.2)
        print(".", end="", flush=True)
    delete_last_line()

def flash_message(msg="Invalid key!", duration=0.5):
    print(msg)
    time.sleep(duration)
    delete_last_line()

# ---------------- EXIT ----------------
def exit_sequence():
    print("Goodbye", end="", flush=True)
    for _ in range(5):
        time.sleep(0.2)
        print(".", end="", flush=True)
    sys.exit()

# ---------------- REGISTER ----------------
def register():
    print("\n=== Register ===")
    username = input("Enter username: ").strip()
    
    while len(username) == 0:
        flash_message("Invalid username, try again.")
        username = input("Enter username: ").strip()
    
    with open(DB_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_usernames = [row["username"] for row in reader]
    
    while username in existing_usernames:
        flash_message("Username taken, try another one.")
        username = input("Enter username: ").strip()

    password = input_password("Enter password: ")
    password_confirm = input_password("Confirm password: ")
    
    while password != password_confirm or len(password) == 0:
        flash_message("Passwords don't match or empty. Try again.")
        password = input_password("Enter password: ")
        password_confirm = input_password("Confirm password: ")
    
    with open(DB_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, password])
    
    print("Registration successful!")
    buffer_and_delete_line()

# ---------------- LOGIN ----------------
def login():
    print("\n=== Login ===")
    while True:
        username = input("Enter username: ").strip()
        password = input_password("Enter password: ")

        with open(DB_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    print(f"Logged in successfully as {username}!")
                    buffer_and_delete_line()
                    return username
        
        flash_message("Invalid username or password. Try again.")
        delete_last_line()
        delete_last_line()

# ---------------- CHANGE PASSWORD ----------------
def change_password(username):
    print("\n=== Change Password ===")
    while True:
        current = input_password("Enter current password: ")
        
        with open(DB_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            valid = any(row["username"] == username and row["password"] == current for row in reader)
        
        if valid:
            break
        else:
            flash_message("Incorrect current password. Try again.")

    new_pass = input_password("Enter new password: ")
    confirm_pass = input_password("Confirm new password: ")

    while new_pass != confirm_pass or len(new_pass) == 0:
        flash_message("Passwords don't match or empty. Try again.")
        new_pass = input_password("Enter new password: ")
        confirm_pass = input_password("Confirm new password: ")

    rows = []
    with open(DB_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                row["password"] = new_pass
            rows.append(row)

    with open(DB_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password"])
        writer.writeheader()
        writer.writerows(rows)

    print("Password changed successfully!")
    buffer_and_delete_line()

# ---------------- MAIN MENU ----------------
def main_menu():
    print("\n=== CLI Login/Register ===")
    print("Press Esc anytime to exit.")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    
    while True:
        key = msvcrt.getch()
        if key == b'\x1b':
            exit_sequence()
        elif key in {b'1', b'2', b'3'}:
            return key
        else:
            flash_message("Invalid key! Press 1, 2, 3, or Esc.")

# ---------------- POST LOGIN MENU ----------------
def post_login_menu(username):
    while True:
        print(f"\n=== Logged in as {username} ===")
        print("1. Change Password")
        print("2. Logout & Exit")
        
        key = msvcrt.getch()
        if key == b'1':
            change_password(username)
            delete_last_line()
        elif key == b'2':
            exit_sequence()
        else:
            flash_message("Invalid key! Press 1, 2")

# ---------------- MAIN ----------------
def main():
    ensure_db()
    
    while True:
        key = main_menu()
        if key == b'1':
            print("\nYou chose Register")
            register()
        elif key == b'2':
            print("\nYou chose Login")
            username = login()
            post_login_menu(username)
        elif key == b'3':
            exit_sequence()

if __name__ == "__main__":
    main()
