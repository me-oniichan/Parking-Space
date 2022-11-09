import tkinter as tk
from tkinter import font
from tkinter import ttk

HERO_BACKGROUND = "#7f3bff"
HERO_FOREGROUND = "#f5f0ff"
ACTIVE_BG = "#b187ff"
HOVER = "#965eff"


class HeroButton(tk.Canvas):
    def __init__(self, master, text="Click ME", height=70, width=150, bg=HERO_BACKGROUND, fg=HERO_FOREGROUND, command=None, activebg=ACTIVE_BG, hoverbg = HOVER, size = 12):
        super().__init__(master=master, height=height, width=width,
                         borderwidth=0, relief=tk.FLAT, bg=bg, highlightthickness=0, cursor="hand2")
        
        self.radius = height/2
        self.activebg = activebg
        self.hoverbg = hoverbg
        self.bg = bg
        self.font = font.Font(family="Helvetica", weight=font.BOLD, size=size)
        self.commad = command

        self.create_rectangle(0, 0, self.radius, height,
                              fill=master["bg"], width=0)

        self.create_rectangle(width-self.radius, 0, width,
                              height, fill=master["bg"], width=0)

        self.arc2 = self.create_arc((0, 0, height, height), start=90,
                        extent=180, width=0, fill=bg, outline=bg)

        self.arc1 = self.create_arc((width-height, 0, width, height),
                        start=270, extent=180, width=0, fill=bg, outline=bg)

        self.create_text(width/2, height/2, fill=fg, text=text,
                         font=self.font)

        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.bind("<Button-1>", self.click)
        self.bind("<ButtonRelease-1>", self.leave)

    def enter(self, event):
        self.config(bg=self.hoverbg)
        self.itemconfigure(self.arc1, fill=self.hoverbg, outline = self.hoverbg)
        self.itemconfigure(self.arc2, fill=self.hoverbg, outline = self.hoverbg)
    
    def leave(self, event):
        self["bg"] = self.bg
        self.itemconfigure(self.arc1, fill=self.bg, outline=self.bg)
        self.itemconfigure(self.arc2, fill=self.bg, outline=self.bg)
    
    def click(self, event):
        self["bg"] = self.activebg
        self.itemconfigure(self.arc1, fill=self.activebg, outline = self.activebg)
        self.itemconfigure(self.arc2, fill=self.activebg, outline = self.activebg)
        self.commad()
        
    
class Entry(tk.Frame):
    def __init__(self,master, **kwargs):
        super().__init__(master, bg = kwargs["bg"])
        self.entry = tk.Entry(self, **kwargs)
        self.entry.pack()
        tk.Frame(self, height=1, bg=HERO_BACKGROUND).pack(fill=tk.X)

class Login(tk.Frame):
    def __init__(self,fg, **kwargs):
        super().__init__(**kwargs)
        self.font = font.Font(family="Consolas", size=10)
        self.userFrame = tk.Frame(self, bg=kwargs["bg"])
        self.userFrame.pack(pady=3)

        tk.Label(self.userFrame, text="Username : ", bg=kwargs["bg"], foreground=fg, font=self.font).pack(side=tk.LEFT)
        self.username  = Entry(self.userFrame, bg=kwargs["bg"], fg=fg, relief='flat', insertbackground=fg, font=self.font)
        self.username.pack(side=tk.RIGHT)

        self.passFrame = tk.Frame(self, bg=kwargs["bg"])
        self.passFrame.pack(pady=3)

        tk.Label(self.passFrame, text="Password : ", bg=kwargs["bg"], foreground=fg, font=self.font).pack(side=tk.LEFT)
        self.passname  = Entry(self.passFrame, bg=kwargs["bg"], fg=fg, relief='flat', insertbackground=fg, font=self.font, show="*")
        self.passname.pack(side=tk.RIGHT)

        HeroButton(master=self, text="Submit", height=35, width=100, size=10).pack(side=tk.BOTTOM, pady=(10,5))


class Signup(Login):
    def __init__(self, fg, **kwargs):
        super().__init__(fg, **kwargs)

        self.confirmPassFrame = tk.Frame(self, bg=kwargs["bg"])
        self.confirmPassFrame.pack(pady=3)
        tk.Label(self.confirmPassFrame, text="Confirm   \nPassword : ", bg=kwargs["bg"], foreground=fg, font=self.font).pack(side=tk.LEFT)
        self.confirmPass = Entry(self.confirmPassFrame, bg=kwargs["bg"], fg=fg, relief='flat', insertbackground=fg, font=self.font, show="*")
        self.confirmPass.pack(side=tk.RIGHT)

class Card(tk.Frame):
    def __init__(self, title, isavailable, id,**kwargs):
        super().__init__(**kwargs, width=900, height=85)
        self.pack_propagate(0)
        self.title = tk.Label(self, text=title, font= font.Font(family="Helvetica", size=17), fg="#aaeeaa", bg=kwargs["bg"])
        self.title.pack(anchor="w", padx=(20,0), pady=(5,0))

        self.bg = "#003d0a" if isavailable else "#3d0000"
        self.fg = "#77ff77" if isavailable else "#ff7777"
        self.text = "Available" if isavailable else "Not Available"

        self.wrapper = tk.Frame(self, bg=kwargs["bg"])
        self.wrapper.pack(anchor="w", pady=(5,0))

        self.available = HeroButton(self.wrapper, text=self.text, size=8, bg=self.bg, fg=self.fg, height=30, width=100, activebg=self.bg, hoverbg=self.bg)
        self.available.pack(side=tk.LEFT, padx=(20,8))

        self.parkid = HeroButton(self.wrapper, text="ID : PID", size=8, bg="#7f37b0", activebg="#7f37b0", hoverbg="#7f37b0", fg=HERO_FOREGROUND, height=30, width=80)
        self.parkid.pack(side=tk.LEFT)