import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Style
import tkinter.messagebox as msg
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)
try:
    import mysql.connector as connection
except ImportError:
    #if mysql coonestor not installed
    err = msg.askyesno("Connection Error", message="mysql-connector not installed, Do you want to install?")
    if err:
        ins = os.system('pip install mysql-connector-python')
    else:
        exit()

class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg = "grey")
        self.login = ttk.Button(self, text="login")
        self.login.pack(side=tk.LEFT)
        self.signup = ttk.Button(self, text="Sign Up")
        self.signup.pack(side=tk.LEFT)

with open("password.txt") as f: password = f.read()
cursor = connection.connect(user="root", password=password, database = "Parking")

root = tk.Tk()
root.geometry("250x250")


windowframe = tk.Frame(root)
windowframe.pack()
StartScreen(windowframe).pack()
root.mainloop()