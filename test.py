import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket
import browserhistory as bh

def host_name():
    print(socket.gethostname())

def history():
    #print(bh.get_browserhistory())
    dict_obj = bh.get_browserhistory()
    print(dict_obj.keys())
   
    #bh.write_browserhistory_csv()
    #file=open("Browserhistory.csv")
    
    print(bh.get_database_paths())
    #print(bh.get_username())
def main(): 
    #karl().mainloop()
    #host_name()
    history()
    
if __name__ == '__main__':
    main()

