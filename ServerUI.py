import tkinter as tk
import tkinter.font as tkFont
import pandas as pd
from functools import partial
from Server import *

LARGE_FONT = ("Verdana", 20)

names = pd.read_csv("database/names.csv")
user = pd.read_csv("database/user.csv")

print(names)

lst_names = [""] + names["name"].tolist()

pages = []


class ServerUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = []

        pages.append(StartPage)
        for i in range(len(lst_names) - 1):
            pages.append(PageOne)

        for i, F in enumerate(pages):
            frame = F(self.container, self, lst_names[i])
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(0)

    def show_frame(self, i):
        frame = self.frames[i]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, name=""):
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

        btn_list = []
        j = 0
        for i, name in enumerate(lst_names[1:]):
            if i % 5 == 0:
                j += 1
            btn_list.append(tk.Button(frame2, text=name, font=LARGE_FONT,
                                    command=partial(controller.show_frame, i+1)))
            btn_list[i].grid(row=j, column=i % 5, padx=10, pady=10)
        '''        btn_name1 = tk.Button(frame2, text="name1", font=LARGE_FONT,
                            command=lambda: controller.show_frame(PageOne))
        btn_name1.grid(row=0, column=0, padx=10, pady=10)'''

    def get_names(self):
        return names["name"].tolist()


class PageOne(tk.Frame):
    def __init__(self, parent, controller, name):
        tk.Frame.__init__(self, parent)
        self.name = name

        frame1 = tk.Frame(self, height=35, bg="pink")
        frame1.pack(fill="both")

        button1 = tk.Button(frame1, text="Back to Home",
                            command=lambda: controller.show_frame(0))
        button1.pack()

        label = tk.Label(frame1, text=f"HELLO {name}!!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


app = ServerUI()
app.geometry("800x700")
app.mainloop()
