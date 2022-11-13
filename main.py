import tkinter as tk
from tkinter import ttk
import utils
from ctypes import windll
import widgets
import tkinter.messagebox as msg
from PIL import ImageTk, Image

#Activate 64 bit display
windll.shcore.SetProcessDpiAwareness(1)

#Global variables 
WIDTH = 1080
HEIGHT = 680
USER = None
OCUUPIED = 0

#Start Screen widget class
class StartScreen(tk.Frame):
    '''
    This class inherits from Tk.Frame and addds additional widgets inside frame.
    This class implements Start Screen window that will display Login and signin options.
    '''
    def __init__(self, master):
        self.master = master
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

        self.loginForm = widgets.Login(command=self.submit_login,master=self.formSpace, fg="#fafafa", bg="#222222")
        self.signupForm = widgets.Signup(command=self.submit_signup, master=self.formSpace, fg="#fafafa", bg="#222222")

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

    def submit_login(self):
        '''Executes when clicked submit from login page. Verifies if user is authentic'''
        global USER, OCUUPIED
        self.user = utils.verify_user(self.loginForm.username.entry.get(), self.loginForm.passname.entry.get())
        if self.user:
            USER = self.user[0]
            utils.cursor.execute(f"select Count(*) from booking where Uid = {USER};")
            OCUUPIED = utils.cursor.fetchone()[0]
            AvailableParking(master=root)
            self.destroy()
        else:
            msg.showwarning("User login fail", message="Username and Password mismatch")
        
    def submit_signup(self):
        """Executes when clicked submit from signup page
           verifies if data is valid or not 
        """
        global USER, OCUUPIED
        self.user = self.signupForm.username.entry.get()
        self.password = self.signupForm.passname.entry.get()
        self.confirmpass = self.signupForm.confirmPass.entry.get()

        self.verify = utils.verify_input(self.user, self.password, self.confirmpass)
        if self.verify == -1:
            msg.showwarning("Password Mismatch", message="Password and confirm password mismatch")
        elif self.verify == -2:
            msg.showwarning("Existing user", message="User already exist!!")
        elif self.verify == 0:
            msg.showwarning("Invalid Username", message="Invalid Username")
        elif self.verify == -3:
            msg.showwarning("Weak Password", message="Password length must be greater than 8 characters")
        else:
            self.res = utils.add_user(self.user, self.password)
            if self.res:
                msg.showinfo("Signup Successful", message="Regestration is succesful. You can login with your username now")
            else:
                msg.showerror("Signup Unsuccessful", message="Couldn't Register")


class AvailableParking(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#323232", height=HEIGHT, width=WIDTH)
        self.pack_propagate(False)
        self.card = None
        self.pack(fill=tk.BOTH, expand=True, ipadx=20, ipady=20)

        self.head = widgets.Header(self, user=USER, occupied=OCUUPIED)
        self.head.pack()

        self.scframe = ScrollableFrame(self)
        self.viewFrame = self.scframe.view
        # self.viewFrame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.refresh_view('all', 0)


    def refresh_view(self, block, ownedOnly):
        self.viewFrame.destroy()
        self.viewFrame = tk.Frame(self.scframe.canvas, bg="#323232", bd=0)
        self.scframe.display_frame(self.viewFrame)
        # self.viewFrame.pack(expand=True, fill=tk.BOTH)
        self.populate(block, ownedOnly)

    def populate(self, block, ownedOnly):
        if not ownedOnly:
            self.data = utils.show_all_parking(block=block)
        else:
            self.data = utils.show_owned(USER, block)
        if self.data:
            for self.i in self.data:
                if self.i[2] == None:
                    self.availibility = 0
                elif self.i[2] == USER.__int__():
                    self.availibility = -1
                else:
                    self.availibility = 1
                    
                widgets.Card(title=f"Block {self.i[1]}", isavailable=self.availibility, id=self.i[0], master=self.viewFrame).pack(padx=5, pady=10)
        else:
            tk.Label(self.viewFrame, text="Nothing to see here.", font='Helvetica 15 bold', bg="#323232", fg="#dddddd").pack(anchor='center', expand=True)


class ScrollableFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=0, bg="#323232")
        self.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self, borderwidth=0, yscrollcommand=self.scrollbar.set, bg="#323232")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        #reset view area
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.view = tk.Frame(self.canvas, bg="#323232", width=WIDTH)
        self.view_ref = self.canvas.create_window(0,0,window=self.view, anchor="n")
   
    def display_frame(self, frame):
        self.view = frame
        frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self.view_ref = self.canvas.create_window(0,0,window=frame, anchor="nw")
        frame.bind("<Configure>", self.onScroll)

    def onScroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.resizable(False, False)
    root.config(bg="#424242")

    style = ttk.Style()
    style.configure("O.TMenubutton", background="#444444", foreground="#ffffff", borderwidth=0, relief="flat", width=5)
    style.configure(("O.TCheckbutton"), background="#444444", foreground="#ffffff", borderwidth=0, relief="flat")
    style.configure("TScrollbar", troughcolor="green")

    start = StartScreen(root)
    root.mainloop()