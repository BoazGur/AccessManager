import tkinter as tk
import tkinter.font as tkFont
from typing import Container
import pandas as pd
from Server import *

LARGE_FONT = ("Verdana", 20)

names = pd.read_csv("database/names.csv")
user = pd.read_csv("database/user.csv")

print(names)


class ServerUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        # args[o] = name of the user
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, *args):
        tk.Frame.__init__(self, parent)
        # -------------------- Welcome Sign
        frame1 = tk.Frame(self, height=35, bg="red")
        frame1.pack(fill="both")

        fnt_welcome = tkFont.Font(size=35)
        lbl_welcome = tk.Label(
            frame1, text="Welcome Manager", font=fnt_welcome)
        lbl_welcome.pack()

        # -------------------- User Buttons
        frame2 = tk.Frame(self, width=100, bg="yellow")
        frame2.pack(fill="both", expand=True)

        names = self.get_names()
        j = 0
        for i, name in enumerate(names):
            if i % 5 == 0:
                j += 1
            btn_name = tk.Button(frame2, text=name, font=LARGE_FONT,
                                 command=lambda: controller.show_frame(PageOne, name))
            btn_name.grid(row=j, column=i % 5, padx=10, pady=10)
        '''        btn_name1 = tk.Button(frame2, text="name1", font=LARGE_FONT,
                              command=lambda: controller.show_frame(PageOne))
        btn_name1.grid(row=0, column=0, padx=10, pady=10)'''

    def get_names(self):
        return names["name"].tolist()

class PageOne(tk.Frame):
    def __init__(self, parent, controller, *args):
        tk.Frame.__init__(self, parent)

        frame1 = tk.Frame(self, height=35, bg="pink")
        frame1.pack(fill="both")

        button1 = tk.Button(frame1, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        try:
            label = tk.Label(frame1, text=f"HELLO {args[0]}!!!!", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
        except:
            label = tk.Label(frame1, text=f"HELLO", font=LARGE_FONT)
            label.pack(pady=10, padx=10)


app = ServerUI()
app.geometry("800x700")
app.mainloop()
