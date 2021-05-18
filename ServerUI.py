from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import pandas as pd
from functools import partial
import os
from Server import *
from urllib import request

LARGE_FONT = ("Verdana", 20)

names = pd.read_csv(os.path.join("database", "names.csv"))


data = {}
for file in os.listdir(os.path.join("database", "customer")):
    filename = file.split(".")[0]
    data[filename] = pd.read_csv(
        os.path.join("database", "customer", f"{file}"))
    data[filename].index += 1

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
        frame1 = tk.Frame(self, height=35, bg="#000018")
        frame1.pack(fill="both")

        fnt_welcome = tkFont.Font(size=35)
        lbl_welcome = tk.Label(
            frame1, text="Welcome Manager", font=fnt_welcome)
        lbl_welcome.pack()

        # -------------------- User Buttons
        frame2 = tk.Frame(self, width=100, bg="#faffff")
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
        self.data = data[name]
        self.search_val = StringVar()
        self.id_val = StringVar()
        self.url_val = StringVar()
        self.name_val = StringVar()
        self.date_val = StringVar()
        self.blocked_val = StringVar()
        self.perm_val = StringVar()
        self.start_val = StringVar()
        self.end_val = StringVar()

        # -----------------------Welcome to name frame
        frame1 = tk.Frame(self, height=35, bg="#006aff")
        frame1.pack(fill="both")

        button1 = tk.Button(frame1, text="Back to Home",
                            command=lambda: controller.show_frame(0))
        button1.pack()

        label = tk.Label(frame1, text=f"{name}", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #-----------------------Table and More
        frame2 = tk.Frame(self, bg="#000009")
        frame2.pack(fill="both", expand=True)

        wrapper1 = tk.LabelFrame(
            frame2, text="Browse History And Blocked Sites")
        wrapper2 = tk.LabelFrame(frame2, text="Search")
        wrapper3 = tk.LabelFrame(frame2, text="Blocked Site Data")

        wrapper1.pack(fill="both", expand=True, padx=20, pady=10)
        wrapper2.pack(fill="both", expand=True, padx=20, pady=10)
        wrapper3.pack(fill="both", expand=True, padx=20, pady=10)

        # -----Table
        self.trv = ttk.Treeview(wrapper1, columns=(
            1, 2, 3, 4, 5, 6, 7, 8), show="headings", height=6)
        self.trv.pack()

        self.trv.heading(1, text="ID")
        self.trv.heading(2, text="URL")
        self.trv.heading(3, text="Site Name")
        self.trv.heading(4, text="Date")
        self.trv.heading(5, text="Blocked")
        self.trv.heading(6, text="Permanent")
        self.trv.heading(7, text="Start")
        self.trv.heading(8, text="End")

        self.trv.bind("<Double 1>", self.get_row)

        self.update_table()

        # -----Search
        lbl_search = tk.Label(wrapper2, text="Search")
        lbl_search.pack(side="left", padx=10)

        ent_search = tk.Entry(wrapper2, textvariable=self.search_val)
        ent_search.pack(side="left", padx=6)

        btn_search = tk.Button(wrapper2, text="Search", command=self.search)
        btn_search.pack(side="left", padx=6)

        btn_clear = tk.Button(wrapper2, text="Clear", command=self.update_table)
        btn_clear.pack(side="left", padx=6)

        # -----Blocked Site Data
        lbl_id = tk.Label(wrapper3, text="ID")
        lbl_id.grid(row=0, column=0, padx=5, pady=3)
        self.ent_id = tk.Entry(wrapper3, textvariable=self.id_val)
        self.ent_id.grid(row=0, column=1, padx=5, pady=3)

        lbl_url = tk.Label(wrapper3, text="URL")
        lbl_url.grid(row=1, column=0, padx=5, pady=3)
        self.ent_url = tk.Entry(wrapper3, textvariable=self.url_val)
        self.ent_url.grid(row=1, column=1, padx=5, pady=3)

        lbl_name = tk.Label(wrapper3, text="Name")
        lbl_name.grid(row=2, column=0, padx=5, pady=3)
        self.ent_name = tk.Entry(wrapper3, textvariable=self.name_val)
        self.ent_name.grid(row=2, column=1, padx=5, pady=3)

        lbl_date = tk.Label(wrapper3, text="Date")
        lbl_date.grid(row=3, column=0, padx=5, pady=3)
        self.ent_date = tkcalendar.DateEntry(wrapper3, textvariable=self.date_val)
        self.ent_date.grid(row=3, column=1, padx=5, pady=3)

        lbl_blocked = tk.Label(wrapper3, text="Blocked")
        lbl_blocked.grid(row=4, column=0, padx=5, pady=3)
        self.ent_blocked = tk.Entry(wrapper3, textvariable=self.blocked_val)
        self.ent_blocked.grid(row=4, column=1, padx=5, pady=3)

        lbl_perm = tk.Label(wrapper3, text="Permanent")
        lbl_perm.grid(row=5, column=0, padx=5, pady=3)
        self.ent_perm = tk.Entry(wrapper3, textvariable=self.perm_val)
        self.ent_perm.grid(row=5, column=1, padx=5, pady=3)

        lbl_start = tk.Label(wrapper3, text="Start")
        lbl_start.grid(row=6, column=0, padx=5, pady=3)
        self.ent_start = tk.Entry(wrapper3, textvariable=self.start_val)
        self.ent_start.grid(row=6, column=1, padx=5, pady=3)

        lbl_end = tk.Label(wrapper3, text="End")
        lbl_end.grid(row=7, column=0, padx=5, pady=3)
        self.ent_end = tk.Entry(wrapper3, textvariable=self.end_val)
        self.ent_end.grid(row=7, column=1, padx=5, pady=3)

        btn_update = tk.Button(wrapper3, text="Update",
                               command=self.update_site)
        btn_add = tk.Button(wrapper3, text="Add New", command=self.add_site)
        btn_delete = tk.Button(wrapper3, text="Delete",
                               command=self.delete_site)
        btn_clear_entries = tk.Button(wrapper3, text="Clear Entries",
                                      command=self.clear_entries)

        btn_add.grid(row=8, column=0, padx=5, pady=3)
        btn_update.grid(row=8, column=1, padx=5, pady=3)
        btn_delete.grid(row=8, column=2, padx=5, pady=3)
        btn_clear_entries.grid(columnspan=3, sticky="ew", padx=5, pady=3)

    def clear_entries(self):
        self.ent_id.delete(0, END)
        self.ent_url.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_date.delete(0, END)
        self.ent_blocked.delete(0, END)
        self.ent_perm.delete(0, END)
        self.ent_start.delete(0, END)
        self.ent_end.delete(0, END)

    def delete_site(self):
        site_id = self.id_val.get()
        if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this site?"):
            self.data = self.data[self.data.index != int(site_id)]
            self.data.to_csv(os.path.join(
                "database", "customer", f"{self.name}.csv"), index=False)
            self.update_table()
            self.clear_entries()
        else:
            return True

    def add_site(self):
        url = self.url_val.get()
        name = self.name_val.get()
        date = self.date_val.get()
        blocked = self.date_val.get()
        perm = self.perm_val.get()
        start = self.start_val.get()
        end = self.end_val.get()

        if messagebox.askyesno("Confirm Addition?", "Are you sure you want to add this site?"):
            if blocked == "True":
                while True:
                    if self.is_valid_url(url):
                        if perm == True:
                            Server.add_limit(url, -1, 25)
                        else:
                            Server.add_limit(url, start, end)
                        break
                    else:
                        messagebox.showerror(
                            "Not Valid URL", "The URL you entered is invalid please try again!")

        self.data = self.data.append({"url": url, "name": name, "date": date, "blocked": blocked,
                                      "perm": perm, "start": start, "end": end}, ignore_index=True)
        self.data.to_csv(os.path.join("database", "customer",
                                      f"{self.name}.csv"), index=False)
        self.update_table()
        self.clear_entries()

    def update_site(self):
        id = self.id_val.get()
        url = self.url_val.get()
        name = self.name_val.get()
        date = self.date_val.get()
        blocked = self.blocked_val.get()
        perm = self.perm_val.get()
        start = self.start_val.get()
        end = self.end_val.get()

        if messagebox.askyesno("Confirm Update?", "Are you sure you want to update this site?\nMake sure the ID matches the record."):
            if (blocked == True) and (self.data.loc[self.data.index == id, "blocked"] == False)[0]:
                if self.is_valid_url(url):
                    if perm == True:
                        Server.limitation("add url", url, -1, 25)
                    else:
                        Server.limitation("add url", url, start, end)
                else:
                    messagebox.showerror(
                        "Not Valid URL", "The URL you entered is invalid please try again! Make sure you don't forget http://.")
            elif (blocked == False) and (self.data.loc[self.data.index == id, "blocked"] == True)[0]:
                Server.limitation("remove url", url, start, end)

            self.data.loc[self.data.index == 1, ["url", "name", "date", "blocked",
                                                  "perm", "start", "end"]] = [url, name, date, blocked, perm, start, end]
            self.data.to_csv(os.path.join(
                "database", "customer", f"{self.name}.csv"), index=False)
            self.update_table()
            self.clear_entries()
        else:
            return True

    def get_row(self, event):
        row_id = self.trv.identify_row(event.y)
        item = self.trv.item(self.trv.focus())
        self.id_val.set(item["values"][0])
        self.url_val.set(item["values"][1])
        self.name_val.set(item["values"][2])
        self.date_val.set(item["values"][3])
        self.blocked_val.set(item["values"][4])
        self.perm_val.set(item["values"][5])
        self.start_val.set(item["values"][6])
        self.end_val.set(item["values"][7])

    def update_table(self):
        self.update(self.data.itertuples())

    def search(self):
        search_val2 = self.search_val.get()
        possible = self.data[self.data["name"].str.contains(search_val2)]
        self.update(possible.itertuples())

    def update(self, rows):
        self.trv.delete(*self.trv.get_children())
        for i in rows:
            self.trv.insert('', 'end', value=i)

    def is_valid_url(self, url):
        try:
            request.urlopen(url)
        except Exception:
            return False

        return True


app = ServerUI()
app.title("Access Manager")
app.geometry("1700x800")
app.mainloop()
