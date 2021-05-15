import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket
import browserhistory as bh
import  sys
import os
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

def ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)

def folder_test():
    print(os.listdir("D:\Python_Code_11\Access_Manager\database"))

def path():
    starting_path=os.path.abspath(os.getcwd())
    print(starting_path)
    
def main(): 
    history()
    #ip()
    #folder_test()

    
if __name__ == '__main__':
    main()

