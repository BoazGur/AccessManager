from tkinter import *
from Server import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import pandas as pd
from functools import partial

import os,time
from urllib import request
from threading import Thread


LARGE_FONT = ("Verdana", 20)
data = {}
pages = []


class ServerUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        """
        Initiates all pages for each name in the name list
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # path_names=os.path.join("database", "names.csv")
        # if not os.path.exists(path_names):
        #     os.makedirs(path_names)
        names = pd.read_csv(os.path.join("database", "names.csv"))

        self.lst_names = [""] + names["name"].tolist()
        
        self.frames = []
        pages.append(StartPage)
        for i in range(len(self.lst_names) - 1):
            pages.append(PageOne)

        for i, F in enumerate(pages):
            frame = F(self.container, self, self.lst_names[i])
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(0)

    def show_frame(self, i):
        """
        Show page
        """
        frame = self.frames[i]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, name=""):
        """
        Main page that directs to all the other pages
        """
        names = pd.read_csv(os.path.join("database", "names.csv"))
        self.lst_names = [""] + names["name"].tolist()
       
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
        for i, name in enumerate(self.lst_names[1:]):
            if i % 5 == 0:
                j += 1
            btn_list.append(tk.Button(frame2, text=name, font=LARGE_FONT,
                                      command=partial(controller.show_frame, i+1)))
            btn_list[i].grid(row=j, column=i % 5, padx=10, pady=10)


    def get_names(self):
        """
        Gets all names
        """
        return names["name"].tolist()


class PageOne(tk.Frame):
    def __init__(self, parent, controller, name):
        """
        Initiates the name page including a table of history, searching option and also editing options
        """
        tk.Frame.__init__(self, parent)
        self.name = name
        self.data = data[name]
        self.search_val = StringVar()
        self.id_val = StringVar()
        self.url_val = StringVar()
        self.name_val = StringVar()
        self.date_val = StringVar()
        self.blocked_val = BooleanVar()
        self.perm_val = BooleanVar()
        self.start_val = StringVar()
        self.end_val = StringVar()
        self.server=server
        
        # -----------------------Welcome to name frame
        frame1 = tk.Frame(self, height=35, bg="#006aff")
        frame1.pack(fill="both")

        button1 = tk.Button(frame1, text="Back to Home",
                            command=lambda: controller.show_frame(0))
        button1.pack(fill="y", side="left", padx=10, pady=10)
        
        button2_refresh = tk.Button(frame1, text="Refresh",
                            command= self.update_table)
        button2_refresh.pack(fill="y", side="right", padx=10, pady=10)
        


        label = tk.Label(frame1, text=f"{name}", font=LARGE_FONT)
        label.pack(side="bottom", pady=10, padx=10)

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
        trv_scrolly = Scrollbar(wrapper1) 
        trv_scrolly.pack(side="right", fill="y")

        trv_scrollx = Scrollbar(wrapper1, orient="horizontal")
        trv_scrollx.pack(side="bottom", fill="x")

        columns = [i for i in range(1, 9)]
        self.trv = ttk.Treeview(wrapper1, columns=columns,
                                show="headings", height=12, yscrollcommand=trv_scrolly.set, xscrollcommand=trv_scrollx.set)
        self.trv.pack()

        trv_scrolly.config(command=self.trv.yview)
        trv_scrollx.config(command=self.trv.xview)

        self.trv.heading(1, text="ID")
        self.trv.heading(2, text="URL")
        self.trv.heading(3, text="Site Name")
        self.trv.heading(4, text="Date")
        self.trv.heading(5, text="Blocked",
                         command=lambda: self.treeview_sort_column(5, False))
        self.trv.heading(6, text="Permanent",
                         command=lambda: self.treeview_sort_column(6, False))
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

        btn_clear = tk.Button(wrapper2, text="Clear",
                              command=self.update_table)
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
        self.ent_date = tkcalendar.DateEntry(
            wrapper3, textvariable=self.date_val)
        self.ent_date.grid(row=3, column=1, padx=5, pady=3)

        lbl_blocked = tk.Label(wrapper3, text="Blocked")
        lbl_blocked.grid(row=4, column=0, padx=5, pady=3)
        self.check_box_blocked = tk.Checkbutton(
            wrapper3, variable=self.blocked_val, onvalue=True, offvalue=False, command=self.hide_perm)
        self.check_box_blocked.grid(row=4, column=1, padx=5, pady=3)

        lbl_perm = tk.Label(wrapper3, text="Permanent")
        lbl_perm.grid(row=5, column=0, padx=5, pady=3)
        self.check_box_perm = tk.Checkbutton(
            wrapper3, variable=self.perm_val, onvalue=True, offvalue=False, state="disabled", command=self.hide_time)
        self.check_box_perm.grid(row=5, column=1, padx=5, pady=3)

        lbl_start = tk.Label(wrapper3, text="Start")
        lbl_start.grid(row=6, column=0, padx=5, pady=3)
        self.ent_start = tk.Entry(
            wrapper3, textvariable=self.start_val, state="disabled")
        self.ent_start.grid(row=6, column=1, padx=5, pady=3)

        lbl_end = tk.Label(wrapper3, text="End")
        lbl_end.grid(row=7, column=0, padx=5, pady=3)
        self.ent_end = tk.Entry(
            wrapper3, textvariable=self.end_val, state="disabled")
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

    def hide_time(self):
        """
        When permanent or blocked is enabled disables use of time entries
        """
        if self.perm_val.get():
            self.ent_start.configure(state="disabled")
            self.ent_end.configure(state="disabled")
        else:
            self.ent_start.configure(state="normal")
            self.ent_end.configure(state="normal")

    def treeview_sort_column(self, col, reverse):
        """
        Sorts rows
        """
        l = [(self.trv.set(k, col), k) for k in self.trv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.trv.move(k, '', index)

        # reverse sort next time
        self.trv.heading(
            col, command=lambda _col=col: self.treeview_sort_column(_col, not reverse))

    def hide_perm(self):
        """
        When blocked is enabled disables use of perm entries
        """
        if self.blocked_val.get():
            self.check_box_perm.configure(state="normal")
            self.ent_start.configure(state="normal")
            self.ent_end.configure(state="normal")
        else:
            self.check_box_perm.configure(state="disabled")
            self.ent_start.configure(state="disabled")
            self.ent_end.configure(state="disabled")

    def clear_entries(self):
        """
        Clear entries
        """
        self.ent_id.delete(0, END)
        self.ent_url.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_date.delete(0, END)
        self.ent_start.delete(0, END)
        self.ent_end.delete(0, END)

    def delete_site(self):
        """
        Deletes the selected site from table, if the site was blocked it unblocks the site 
        """
        site_id = self.id_val.get()
        url = self.url_val.get()
        name = self.name_val.get()
        date = self.date_val.get()
        blocked = self.blocked_val.get()
        perm = self.perm_val.get()
        start = self.start_val.get()
        end = self.end_val.get()
       
        new_row={}
        df_changes= pd.read_csv(os.path.join("database", "customers",f"{self.name}","changes.csv"))
        if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this site?"):
            if blocked==True:
                self.server.limitation("remove url", url, 0, 0)
                
            new_row = {"url":url, "name":name, "date":date, "blocked":"delete", "perm":False, "start":0, "end":0}
            if not df_changes.isin([url]).any().any():# if not exists
                df_changes = df_changes.append(new_row, ignore_index=True)
            else:
                df_changes.loc[df_changes["url"]== url,"blocked"]="delete"
                df_changes.loc[df_changes["url"]== url,"perm"]=False
                df_changes.loc[df_changes["url"]== url,"start"]=0
                df_changes.loc[df_changes["url"]== url,"end"]=23
                
            df_changes.to_csv(os.path.join("database", "customers",f"{self.name}","changes.csv"),index=False)
            self.data = self.data[self.data.index != int(site_id)]
            self.data.to_csv(os.path.join("database", "customers",f"{self.name}","history.csv"), index=False)#TODO change addres
            self.update_table()
            self.clear_entries()
    
    def add_site(self):
        """
        Adds new site to table
        """
        url = self.url_val.get()
        name = self.name_val.get()
        date = self.date_val.get()
        blocked = self.blocked_val.get()
        perm = self.perm_val.get()
        start = self.start_val.get()
        end = self.end_val.get()
        
        df_changes= pd.read_csv(os.path.join("database", "customers",f"{self.name}","changes.csv"))
        new_row={}
        if messagebox.askyesno("Confirm Addition?", "Are you sure you want to add this site?"):
            if blocked == True:
                if self.is_valid_url(url):
                    if perm == True:
                        start=0
                        end=23
                        
                    print("send limit to server")  
                    self.server.limitation("add url", url, start, end)  
                    new_row={"url":url, "name":name, "date":date, "blocked":blocked,"perm":perm, "start":int(start), "end":int(end)}            
                else:
                    messagebox.showerror( "Not Valid URL", "The URL you entered is invalid please try again!")
            else:
                new_row={"url":url, "name":name, "date":date, "blocked":False,"perm":False, "start":0, "end":0}
            
            
            if not df_changes.isin([url]).any().any():# if not exists
                df_changes = df_changes.append(new_row, ignore_index=True)
            else:# change if  exists
                df_changes.loc[df_changes["url"]== url,"blocked"]=blocked
                df_changes.loc[df_changes["url"]== url,"perm"]=perm
                df_changes.loc[df_changes["url"]== url,"start"]=start
                df_changes.loc[df_changes["url"]== url,"end"]=end  
                       
            df_changes.to_csv(os.path.join("database", "customers",f"{self.name}","changes.csv"),index=False) 
            self.update_table()
            self.clear_entries()
            time.sleep(0.5)
 

    def update_site(self):
        """
        Updates site according to what the access manager had decided
        """
        id = self.id_val.get()
        url = self.url_val.get()
        name = self.name_val.get()
        date = self.date_val.get()
        blocked = self.blocked_val.get()
        perm = self.perm_val.get()
        start = self.start_val.get()
        end =self.end_val.get()
        df_changes= pd.read_csv(os.path.join("database", "customers",f"{self.name}","changes.csv"))
        new_row={}
        if id != "":
            if messagebox.askyesno("Confirm Update?", "Are you sure you want to update this site?\nMake sure the ID matches the record."):
                if (blocked == True) and ((self.data.loc[self.data.index == int(id), "blocked"]).tolist()[0] == False):
                    if self.is_valid_url(url)==True:
                        if perm == True:
                            start=0
                            end=23
                        
                        print("send limit to server")
                        self.server.limitation("add url", url, start, end)  
                        new_row={"url":url, "name":name, "date":date, "blocked":blocked,"perm":perm, "start":int(start), "end":int(end)}
                        if not df_changes.isin([url]).any().any():
                            df_changes = df_changes.append(new_row, ignore_index=True)
                        else:
                            df_changes.loc[df_changes["url"]== url,"blocked"]=blocked
                            df_changes.loc[df_changes["url"]== url,"perm"]=perm
                            df_changes.loc[df_changes["url"]== url,"start"]=start
                            df_changes.loc[df_changes["url"]== url,"end"]=end                               
                    else:
                        messagebox.showerror("Not Valid URL", "The URL you entered is invalid please try again! Make sure you don't forget http://.")
                elif (blocked == False) and ((self.data.loc[self.data.index == int(id), "blocked"]).tolist()[0]  == True):
                    print("sending remove")
                    self.server.limitation("remove url", url, 0, 0)
                    df_changes.loc[df_changes["url"]== url,"blocked"]=False
                    df_changes.loc[df_changes["url"]== url,"perm"]=False
                    df_changes.loc[df_changes["url"]== url,"start"]=0
                    df_changes.loc[df_changes["url"]== url,"end"]=0
                    
                df_changes.to_csv(os.path.join("database", "customers",f"{self.name}","changes.csv"),index=False)
                self.update_table()
                self.clear_entries() 
                time.sleep(1)           
        else:
            messagebox.showerror("Invalid Input", "Please select a record (or change ID value) to update the record.")

    def get_row(self, event):
        """
        Gets selected row 
        """
        item = self.trv.item(self.trv.focus())
        try:
            self.id_val.set(item["values"][0])
        except IndexError:
            pass
        self.url_val.set(item["values"][1])
        self.name_val.set(item["values"][2])
        self.date_val.set(item["values"][3])
        self.blocked_val.set(bool(item["values"][4]))
        self.perm_val.set(bool(item["values"][5]))
        self.start_val.set(item["values"][6])
        self.end_val.set(item["values"][7])

        self.hide_perm()
        self.hide_time()

    def update_table(self):
        """
        Refreshes the table
        """
        self.update(self.data.itertuples())

    def search(self):
        """
        Shows the row that matched the search
        """
        search_val2 = self.search_val.get()
        possible = self.data[self.data["name"].str.contains(search_val2)]
        self.update(possible.itertuples())

    def update(self, rows):
        """
        Updates the table
        """
        table=pd.read_csv(os.path.join("database", "customers", f"{self.name}","history.csv"))
        if not table.empty:
            self.data=table

        self.trv.delete(*self.trv.get_children())
        for i, row in enumerate(rows):
            if i % 2 == 0:
                self.trv.insert('', 'end', value=row, tags=("even"))
            else:
                self.trv.insert('', 'end', value=row, tags=("odd"))

        self.trv.tag_configure("even", background="#99cccc")
        self.trv.tag_configure("odd", background="#fff0f5")

    def is_valid_url(self, url):
        """
        Checks if url is valid
        Returns:
            True if valid
        """
        try:
            request.urlopen(url)
        except Exception:
            return False
        
        return True


def ui():
    """
    Initiates the user interface
    """
    
    time.sleep(7)
    path = os.path.join("database", "customers")
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if 'history.csv' in file:
                files.append(os.path.join(r, file))
    for f in files:
        user_name=f.split("\\")[2]
        data[user_name]=pd.read_csv(f)
        #data[user_name] = data[user_name].fillna("")   
            
    app = ServerUI()
    app.title("Access Manager")
    app.geometry("1600x900")
    app.mainloop()

def server_py():
    """
    Initiates the Server.py
    """
    time.sleep(5)
    global server
    server=Server()
    server.get_requests()
  
def find_connection():
    """
    Find  ip for connection
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)
    server.bind(("", 44444))
    message = b"your very important message"
    while True:
        server.sendto(message, ('<broadcast>', 37020))
        # print("message sent!")
        time.sleep(0.1)
        
if __name__ == "__main__":
    Thread(target = ui).start()
    Thread(target = find_connection).start()
    Thread(target = server_py).start()