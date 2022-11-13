import tkinter as tk
from tkinter import font
from tkinter import ttk
import utils

HERO_BACKGROUND = "#7f3bff"
HERO_FOREGROUND = "#f5f0ff"
ACTIVE_BG = "#b187ff"
HOVER = "#965eff"


class HeroButton(tk.Canvas):
    def __init__(self, master, text="Click ME", height=70, width=150, bg=HERO_BACKGROUND, fg=HERO_FOREGROUND,
                 command=None, activebg=ACTIVE_BG, hoverbg=HOVER, size=12):
        super().__init__(master=master, height=height, width=width,
                         borderwidth=0, relief=tk.FLAT, bg=bg, highlightthickness=0, cursor="hand2")

        self.radius = height / 2
        self.activebg = activebg
        self.hoverbg = hoverbg
        self.bg = bg
        self.font = font.Font(family="Helvetica", weight=font.BOLD, size=size)
        self.command = command

        self.create_rectangle(0, 0, self.radius, height,
                              fill=master["bg"], width=0)

        self.create_rectangle(width - self.radius, 0, width,
                              height, fill=master["bg"], width=0)

        self.arc2 = self.create_arc((0, 0, height, height), start=90,
                                    extent=180, width=0, fill=bg, outline=bg)

        self.arc1 = self.create_arc((width - height, 0, width, height),
                                    start=270, extent=180, width=0, fill=bg, outline=bg)

        self.create_text(width / 2, height / 2, fill=fg, text=text,
                         font=self.font)

        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.bind("<Button-1>", self.click)
        self.bind("<ButtonRelease-1>", self.leave)

    def enter(self, event):
        self.config(bg=self.hoverbg)
        self.itemconfigure(self.arc1, fill=self.hoverbg, outline=self.hoverbg)
        self.itemconfigure(self.arc2, fill=self.hoverbg, outline=self.hoverbg)

    def leave(self, event):
        self["bg"] = self.bg
        self.itemconfigure(self.arc1, fill=self.bg, outline=self.bg)
        self.itemconfigure(self.arc2, fill=self.bg, outline=self.bg)

    def click(self, event):
        self["bg"] = self.activebg
        self.itemconfigure(self.arc1, fill=self.activebg,
                           outline=self.activebg)
        self.itemconfigure(self.arc2, fill=self.activebg,
                           outline=self.activebg)
        if self.command:
            self.command()


class Entry(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=kwargs["bg"])
        self.entry = tk.Entry(self, **kwargs)
        self.entry.pack()
        tk.Frame(self, height=1, bg=HERO_BACKGROUND).pack(fill=tk.X)


class Login(tk.Frame):
    def __init__(self, command, fg, **kwargs):
        super().__init__(**kwargs)
        self.font = font.Font(family="Consolas", size=10)
        self.userFrame = tk.Frame(self, bg=kwargs["bg"])
        self.userFrame.pack(pady=3)

        tk.Label(self.userFrame, text="Username : ",
                 bg=kwargs["bg"], foreground=fg, font=self.font).pack(side=tk.LEFT)
        self.username = Entry(self.userFrame, bg=kwargs["bg"], fg=fg, relief='flat', insertbackground=fg,
                              font=self.font)
        self.username.pack(side=tk.RIGHT)

        self.passFrame = tk.Frame(self, bg=kwargs["bg"])
        self.passFrame.pack(pady=3)

        tk.Label(self.passFrame, text="Password : ",
                 bg=kwargs["bg"], foreground=fg, font=self.font).pack(side=tk.LEFT)
        self.passname = Entry(self.passFrame, bg=kwargs["bg"], fg=fg, relief='flat', insertbackground=fg,
                              font=self.font, show="*")
        self.passname.pack(side=tk.RIGHT)

        self.submit = HeroButton(master=self, text="Submit", height=35, width=100, command=command,
                                 size=10).pack(side=tk.BOTTOM, pady=(10, 5))


class Signup(Login):
    def __init__(self, command, fg, **kwargs):
        super().__init__(command, fg, **kwargs)

        self.confirmPassFrame = tk.Frame(self, bg=kwargs["bg"])
        self.confirmPassFrame.pack(pady=3)
        tk.Label(self.confirmPassFrame, text="Confirm   \nPassword : ", bg=kwargs["bg"], foreground=fg,
                 font=self.font).pack(side=tk.LEFT)
        self.confirmPass = Entry(self.confirmPassFrame, bg=kwargs["bg"], fg=fg, relief='flat', insertbackground=fg,
                                 font=self.font, show="*")
        self.confirmPass.pack(side=tk.RIGHT)


class Card(tk.Frame):
    def __init__(self, title, isavailable, id, **kwargs):
        if isavailable == 0:
            self.bg = "#3d0000"
            self.fg = "#ff7777"
            self.text = "Not Available"
            self.cardbg = "#424242"
        elif isavailable == 1:
            self.bg = "#003d0a"
            self.fg = "#77ff77"
            self.text = "Available"
            self.cardbg = "#424242"

        elif isavailable == -1:
            self.bg = "#00607d"
            self.fg = "#21f4ff"
            self.text = "Owned"
            self.cardbg = "#3b1869"

        super().__init__(**kwargs, width=900, height=85, bg=self.cardbg)
        self.pack_propagate(False)

        self.wrapper = tk.Frame(self, bg=self.cardbg)
        self.wrapper.pack(side=tk.LEFT, pady=(0, 0))

        self.title = tk.Label(self.wrapper, text=title, font=font.Font(family="Helvetica", size=15), fg=self.fg,
                              bg=self.cardbg)
        self.title.pack(anchor="w", padx=(20, 0), pady=(0, 5))

        self.available = HeroButton(self.wrapper, text=self.text, size=8, bg=self.bg, fg=self.fg, height=30, width=100,
                                    activebg=self.bg, hoverbg=self.bg)
        self.available.pack(side=tk.LEFT, padx=(20, 8))

        self.parkid = HeroButton(self.wrapper, text=f"ID : {id}", size=8, bg="#7f37b0", activebg="#7f37b0",
                                 hoverbg="#7f37b0", fg=HERO_FOREGROUND, height=30, width=80)
        self.parkid.pack(side=tk.LEFT)

        if isavailable == -1:
            self.actionButton = tk.Button(
                self, text="Cancel", bg="#ee4444", fg="#eeeeee", activebackground="#ee4444", activeforeground="#eeeeee")
        elif isavailable == 0:
            self.actionButton = tk.Button(
                self, text="Book", cursor="X_cursor", state=tk.DISABLED, relief=tk.SUNKEN)
        else:
            self.actionButton = tk.Button(
                self, text="Book", bg="#55cc55", fg="black", activebackground="#55cc55", activeforeground="black")

        self.actionButton.config(font="Helvetica 10 bold", width=7, height=2)
        self.actionButton.pack(side=tk.RIGHT, padx=10)


class Header(tk.Frame):
    def __init__(self, master, user, occupied):
        self.bg = "#262626"
        super().__init__(master, bg=self.bg, height=50)
        self.pack_propagate(0)
        self.pack(fill=tk.X)
        self.username = tk.Label(self, bg=self.bg, text=f"User ID : {user}", fg="#efefef",
                                 font=font.Font(family="Impact", size=12))
        self.username.pack(side=tk.LEFT, padx=20)

        self.onlyOwned = tk.IntVar()
        self.checkBox = ttk.Checkbutton(self, variable=self.onlyOwned, text="Only Owned?", width=12,
                                        style="O.TCheckbutton", command=lambda: master.refresh_view(self.value.get(), self.onlyOwned.get()))
        self.checkBox.pack(side="right", padx=5)

        self.blocks = ["", "All", "30",
                       "37", "38", "43", "56", "58", "60"]
        self.value = tk.StringVar()
        self.value.set('All')

        self.option = ttk.OptionMenu(
            self, self.value, *self.blocks, command=lambda e: master.refresh_view(self.value.get(), self.onlyOwned.get()))
        self.option.pack(side=tk.RIGHT, padx=10)
        self.option.config(style="O.TMenubutton", text="Choose Block")

        self.occupied = tk.Label(
            self, text=f"Occupied : {occupied}/3", bg=self.bg, fg="#ffffff", font="Impact 11")
        self.occupied.pack(side=tk.RIGHT, padx=10)
