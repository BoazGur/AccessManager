import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket
import browserhistory as bh

def host_name():
    print(socket.gethostname())

def history():
    print(bh.get_browserhistory())
    #bh.write_browserhistory_csv()
    #file=open("Browserhistory.txt","wt",encoding="utf-8")
def main(): 
    #karl().mainloop()
    #host_name()
    history()
if __name__ == '__main__':
    main()
