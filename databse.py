import os
import random as rn
import tkinter as tk
import tkinter.messagebox as msg
from ctypes import windll
from tkinter import ttk
from uuid import uuid4

# Activate 64 bit display
windll.shcore.SetProcessDpiAwareness(1)

try:
    import mysql.connector as connection
    from mysql.connector import errorcode
except ImportError:
    #if mysql connector not installed
    err = msg.askyesno("Connection Error", message="mysql-connector not installed, Do you want to install?")
    if err:
        ins = os.system('pip install mysql-connector-python')
    else:
        exit()

cursor = None
db = None

def on_closing():
    exit()

def select_database(cur):
    try:
        cur.execute("create database parking;")
    except:
        pass
    finally:
        cur.execute("use parking;")

def verify_tables(cur):
    try:
        cur.execute("create table user(Uid int primary key, Name varchar(25), created date, password varchar(25));")
        cur.execute("create table parking_space(Pid char(4) primary key, block int);")
        cur.execute("create table booking(Uid int, Pid char(4) primary key, date date, time int, constraint fk_uid foreign key (Uid) REFERENCES user(Uid), constraint fk_pid foreign key (Pid) REFERENCES parking_space(Pid));")

        ##pupulate fake data into database
        for i in range(100):
            cursor.execute(f"insert into user values({12114100 + i}, '{str(uuid4())[:5]}', '2022-11-10', '123456');")
        db.commit()

        mylist = ["37", "38", "43", "56", "58", "60"]
        ids = []
        for i in range(20):
            id = str(uuid4())[:4]
            ids.append(id)
            cursor.execute(f"insert into parking_space values('{id}', '{rn.choice(mylist)}');")

        for i in range(10):
            cursor.execute(f"insert into booking values({12114100 + i}, '{ids[i]}', '2022-11-10', {1300+i})")
        db.commit()
    except:
        pass

def connect(username, password):
    global cursor, db
    try:
        db = connection.connect(user=username, password=password)
        cursor = db.cursor()
        select_database(cur=cursor)
        verify_tables(cursor)
        win.destroy()
    except connection.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            msg.showerror("Error", message="Invalid credentials")
        else:
            print(err)
            msg.showerror("Error", message="Corrupt mysql installation")

try:
    win = tk.Tk()
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.config(padx=20, pady=20)
    win.title("Mysql Connector")
    frame1 = tk.Frame(win)
    frame1.pack()

    frame2 = tk.Frame(win)
    frame2.pack()

    ttk.Label(frame1, text="Username : ").pack(side=tk.LEFT)
    username = ttk.Entry(frame1)
    username.pack(side=tk.RIGHT, padx=5, pady=5)

    ttk.Label(frame2, text="Password :  ").pack(side=tk.LEFT)
    password = ttk.Entry(frame2, show="*")
    password.pack(side=tk.RIGHT, padx=5, pady=5)

    submit = ttk.Button(win, text="Submit", command= lambda : connect(username.get(), password.get())).pack(pady=(20,5))
    win.mainloop()
except Exception as e:
    msg.showerror("Connection Error", message="Unable to connect MySQL")
    exit()
