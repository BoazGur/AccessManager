import tkinter as tk
import tkinter.font as tkFont
import sqlite3

LARGE_FONT = ("Verdana", 20)

conn = sqlite3.connect("manager.db")
c = conn.cursor()


class ServerUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
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

        btn_name1 = tk.Button(frame2, text="name1", font=LARGE_FONT,
                              command=lambda: controller.show_frame(PageOne))
        btn_name1.grid(row=0, column=0, padx=10, pady=10)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame1 = tk.Frame(self, height=35, bg="pink")
        frame1.pack(fill="both")

        button1 = tk.Button(frame1, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        label = tk.Label(frame1, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)



app = ServerUI()
app.geometry("800x700")
app.mainloop()

conn.commit()
conn.close()