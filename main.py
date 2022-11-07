import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Style
import tkinter.messagebox as msg
from ctypes import windll
import widgets

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
        super().__init__(master, bg = "#424242")
        self.login = widgets.HeroButton(self, "Login")
        self.login.pack(side=tk.LEFT, fill=tk.BOTH)

        self.signup = widgets.HeroButton(self, "Signup")
        self.signup.pack(side=tk.LEFT, fill=tk.BOTH, anchor="center")
        
        self.pack(fill="both")

with open("password.txt") as f: password = f.read()
cursor = connection.connect(user="root", password=password, database = "Parking")

WIDTH = 1080
HEIGHT = 680

root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)


# windowframe = tk.Frame(root, bg="#424242", height=HEIGHT, width=WIDTH)
# windowframe.pack_propagate(0)
# windowframe.pack(fill=tk.BOTH)
start = StartScreen(root)
root.mainloop()