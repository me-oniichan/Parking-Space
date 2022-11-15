import tkinter.messagebox as msg
import tkinter as tk
from tkinter import ttk
import os
try:
    import mysql.connector as connection
except ImportError:
    #if mysql connector not installed
    err = msg.askyesno("Connection Error", message="mysql-connector not installed, Do you want to install?")
    if err:
        ins = os.system('pip install mysql-connector-python')
    else:
        exit()

cursor = None
db = None
def connect(username, password):
    global cursor, db
    try:
        db = connection.connect(user=username, password=password, database="Parking")
        cursor = db.cursor()
        win.destroy()
    except:
        msg.showerror("Error", message="Invalid credentials")

try:
    win = tk.Tk()
    frame1 = tk.Frame(win)
    frame1.pack()

    frame2 = tk.Frame(win)
    frame2.pack()

    ttk.Label(frame1, text="Username : ").pack(side=tk.LEFT)
    username = ttk.Entry(frame1)
    username.pack(side=tk.RIGHT, padx=5, pady=5)

    ttk.Label(frame2, text="Password : ").pack(side=tk.LEFT)
    password = ttk.Entry(frame2, show="*")
    password.pack(side=tk.RIGHT, padx=5, pady=5)

    submit = tk.Button(win, text="Submit", command= lambda : connect(username.get(), password.get())).pack()
    win.mainloop()
except Exception as e:
    msg.showerror("Connection Error", message="Unable to connect MySQL")
    exit()