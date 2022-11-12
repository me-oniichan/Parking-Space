import tkinter.messagebox as msg
import os
try:
    import mysql.connector as connection
except ImportError:
    # if mysql connector not installed
    err = msg.askyesno("Connection Error", message="mysql-connector not installed, Do you want to install?")
    if err:
        ins = os.system('pip install mysql-connector-python')
    else:
        exit()

try:
    with open("password.txt") as f:
        password = f.read()
    db = connection.connect(user="root", password=password, database="Parking")
    cursor = db.cursor()
except Exception as e:
    msg.showerror("Connection Error", message="Unable to connect MySQL")
    exit()