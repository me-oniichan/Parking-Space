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
    # if mysql connector not installed
    err = msg.askyesno("Connection Error", message="mysql-connector not installed, Do you want to install?")
    if err:
        ins = os.system('pip install mysql-connector-python')
    else:
        exit()


class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#424242", height=HEIGHT)

        # utility vars
        self.log = 0
        self.sign = 0

        self.pack(fill=tk.BOTH, expand=True)

        self.buttonFrame = tk.Frame(self, bg="#424242", height=HEIGHT)
        self.buttonFrame.pack(anchor="center", expand=True, side=tk.LEFT, fill=tk.Y)

        self.tophalf = tk.Frame(self.buttonFrame, bg="#424242")
        self.tophalf.pack(pady=(100, 0))
        self.logo = Image.open("images/parking-logo.png").resize((int(250 * 1.5), 250))
        self.logo = ImageTk.PhotoImage(self.logo)
        tk.Label(self.tophalf, image=self.logo, bg=self.tophalf["bg"]).pack()

        self.formSpace = tk.Frame(self.buttonFrame, bg="#424242", width=300)

        self.formSpace.pack(side=tk.BOTTOM, expand=True, pady=10, anchor="n")

        self.login = widgets.HeroButton(self.tophalf, "Login", size=12, command=self.login_clicked)
        self.login.pack(side=tk.LEFT, padx=30)

        self.signup = widgets.HeroButton(self.tophalf, "Signup", size=12, command=self.signup_clicked)
        self.signup.pack(side=tk.LEFT)

        self.bgimg = Image.open("images/parking.png")
        self.bgimg = ImageTk.PhotoImage(self.bgimg.resize((900, HEIGHT)))
        tk.Label(self, image=self.bgimg, borderwidth=0, width=600).pack(side=tk.RIGHT)

        self.loginForm = widgets.Login(master=self.formSpace, fg="#fafafa", bg="#222222")
        self.signupForm = widgets.Signup(master=self.formSpace, fg="#fafafa", bg="#222222")

    def show_login(self):
        self.loginForm.pack(ipadx=20, pady=10)
        self.log = 1

    def show_signup(self):
        self.signupForm.pack(ipadx=20, pady=10)
        self.sign = 1

    def collapse_login(self):
        self.loginForm.pack_forget()
        self.log = 0

    def collapse_signup(self):
        self.signupForm.pack_forget()
        self.sign = 0

    def login_clicked(self):
        if self.sign: self.collapse_signup()
        if self.log:
            self.collapse_login()
        else:
            self.show_login()

    def signup_clicked(self):
        if self.log: self.collapse_login()
        if self.sign:
            self.collapse_signup()
        else:
            self.show_signup()


class AvailableParking(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#323232", height=HEIGHT)
        self.card = None
        self.pack(fill=tk.BOTH, expand=True, ipadx=20, ipady=20)

        self.head = widgets.Header(self, user="12114156")
        self.head.pack()

        self.viewFrame = tk.Frame(self, bg="#323232")
        self.viewFrame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.switch = 0
        self.refresh_view(self.switch)

    def refresh_view(self, switch):
        self.viewFrame.destroy()
        self.viewFrame = tk.Frame(self, bg="#323232")
        self.viewFrame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        if switch:
            self.populate()
            self.switch = 0
        else:
            self.dummy()
            self.switch = 1

    def populate(self):
        self.card = widgets.Card(title="Block 34", isavailable=1, id=0, master=self.viewFrame)
        self.card.pack(padx=5, pady=10)

        self.card = widgets.Card(title="Block 34", isavailable=0, id=0, master=self.viewFrame)
        self.card.pack(padx=5, pady=10)

        self.card = widgets.Card(title="Block 34", isavailable=-1, id=0, master=self.viewFrame)
        self.card.pack(padx=5, pady=10)

    def dummy(self):
        self.card = widgets.Card(title="Block 34", isavailable=-1, id=0, master=self.viewFrame)
        self.card.pack(padx=5, pady=10)

        self.card = widgets.Card(title="Block 34", isavailable=1, id=0, master=self.viewFrame)
        self.card.pack(padx=5, pady=10)

        self.card = widgets.Card(title="Block 34", isavailable=-0, id=0, master=self.viewFrame)
        self.card.pack(padx=5, pady=10)


if __name__ == "__main__":
    try:
        with open("password.txt") as f:
            password = f.read()
        cursor = connection.connect(user="root", password=password, database="Parking")
    except:
        msg.showerror("Connection Error", message="Unable to connect MySQL")
        exit()

    WIDTH = 1080
    HEIGHT = 680

    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(False, False)
    root.config(bg="#424242")

    style = ttk.Style()
    style.configure("O.TMenubutton", background="#444444", foreground="#ffffff", borderwidth=0, relief="flat", width=5)
    style.configure(("O.TCheckbutton"), background="#444444", foreground="#ffffff", borderwidth=0, relief="flat")

    # start = StartScreen(root)
    paking = AvailableParking(master=root)
    root.mainloop()
