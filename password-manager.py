import sqlite3
import bcrypt
from cryptography.fernet import Fernet
import datetime
import random
import string
import re
import os
import getpass

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key","wb") as f: 
        f.write(key)

with open("secret.key","rb") as f:
    key = f.read()

cipher = Fernet(key)

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password_hash TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
service TEXT,
account TEXT,
password TEXT,
expiry DATE
)
""")

conn.commit()

def strong_password(p):
    if len(p) < 8:
        return False
    if not re.search("[A-Z]",p):
        return False
    if not re.search("[a-z]",p):
        return False
    if not re.search("[0-9]",p):
        return False
    if not re.search("[@#$%^&*!]",p):
        return False
    return True

def generate_password():
    chars = string.ascii_letters + string.digits + "@#$%^&*! "
    return ''.join(random.choice(chars) for _ in range(16))

def register():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users(username,password_hash) VALUES (?,?)",(username,hashed))
        conn.commit()
        print("User registered")
    except:
        print("User already exists")

def login():
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    cursor.execute("SELECT id,password_hash FROM users WHERE username=?",(username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode(),user[1]):
        print("Login success")
        return user[0]
    else:
        print("Invalid login")
        return None

def add_password(user_id):

    service = input("Service: ")
    account = input("Account Username: ")

    choice = input("Auto generate password? (y/n): ")

    if choice == "y":
        password = generate_password()
        print("Generated password:",password)
    else:
        password = getpass.getpass("Password: ")

    if not strong_password(password):
        print("Password not strong enough")
        return

    days = int(input("Expiry days: "))
    expiry = datetime.date.today() + datetime.timedelta(days=days)

    encrypted = cipher.encrypt(password.encode())

    cursor.execute("INSERT INTO passwords(user_id,service,account,password,expiry) VALUES (?,?,?,?,?)",
                   (user_id,service,account,encrypted,expiry))

    conn.commit()
    print("Password stored securely")

def list_passwords(user_id):

    cursor.execute("SELECT id,service,account,password,expiry FROM passwords WHERE user_id=?",(user_id,))
    rows = cursor.fetchall()

    for r in rows:

        decrypted = cipher.decrypt(r[3]).decode()

        expiry = datetime.date.fromisoformat(r[4])
        today = datetime.date.today()

        status = "Valid"
        if today > expiry:
            status = "EXPIRED"

        print("\nID:",r[0])
        print("Service:",r[1])
        print("Account:",r[2])
        print("Password:",decrypted)
        print("Expiry:",r[4],status)
        print("---------------------")

def update_password(user_id):

    pid = input("Enter password ID: ")
    newpass = input("New password (or type auto): ")

    if newpass == "auto":
        newpass = generate_password()
        print("Generated:",newpass)

    if not strong_password(newpass):
        print("Weak password")
        return

    encrypted = cipher.encrypt(newpass.encode())

    cursor.execute("UPDATE passwords SET password=? WHERE id=? AND user_id=?",
                   (encrypted,pid,user_id))

    conn.commit()
    print("Password updated")

def delete_password(user_id):

    pid = input("Enter password ID to delete: ")

    cursor.execute("DELETE FROM passwords WHERE id=? AND user_id=?",(pid,user_id))
    conn.commit()

    print("Password deleted")

def menu(user_id):

    while True:

        print("""
1 Add Password
2 List Passwords
3 Update Password
4 Delete Password
5 Generate Password
6 Logout
""")

        choice = input("Choice: ")

        if choice == "1":
            add_password(user_id)

        elif choice == "2":
            list_passwords(user_id)

        elif choice == "3":
            update_password(user_id)

        elif choice == "4":
            delete_password(user_id)

        elif choice == "5":
            print("Generated:",generate_password())

        elif choice == "6":
            break

while True:

    print("""
1 Register
2 Login
3 Exit
""")

    choice = input("Choice: ")

    if choice == "1":
        register()

    elif choice == "2":
        uid = login()
        if uid:
            menu(uid)

    elif choice == "3":
        break