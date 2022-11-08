import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
from ctypes import windll
import widgets
from PIL import ImageTk, Image

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
        super().__init__(master, bg = "#424242", height=HEIGHT)
        self.pack(fill=tk.BOTH, expand=True)

        self.buttonFrame = tk.Frame(self, bg="#424242", height=HEIGHT)
        self.buttonFrame.pack(anchor="center", expand=True, side=tk.LEFT)

        self.logo = Image.open("images/parking-logo.png").resize((int(250*1.5), 250))
        self.logo = ImageTk.PhotoImage(self.logo)
        tk.Label(self.buttonFrame, image=self.logo, bg = self.buttonFrame["bg"]).pack()

        self.formSpace = tk.Frame(self.buttonFrame)
        self.formSpace.pack(side=tk.BOTTOM, pady=10)

        self.login = widgets.HeroButton(self.buttonFrame, "Login")
        self.login.pack(side=tk.LEFT, padx=30)

        self.signup = widgets.HeroButton(self.buttonFrame, "Signup")
        self.signup.pack(side=tk.LEFT)
        
        self.bgimg = Image.open("images/parking.png")
        self.bgimg = ImageTk.PhotoImage(self.bgimg.resize((900, HEIGHT)))
        tk.Label(self, image=self.bgimg, borderwidth=0, width=600).pack(side=tk.RIGHT)

        self.loginForm = widgets.Login(master=self.formSpace, fg="#fafafa",bg = "#222222")
        

if __name__ == "__main__":
    try:
        with open("password.txt") as f: password = f.read()
        cursor = connection.connect(user="root", password=password, database = "Parking")
    except:
        msg.showerror("Connection Error", message="Unable to connect MySQL")
        exit()

    WIDTH = 1080
    HEIGHT = 680

    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(False, False)
    root.config(bg="#424242")

    start = StartScreen(root)
    root.mainloop()