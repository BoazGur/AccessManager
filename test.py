import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket,sys,os,re
import browserhistory as bh
from  urllib import  request
import urllib3
from Server import Server as s
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

def valid():
    resp=None
    try:
        resp=request.urlopen("https://www.google.co.il/?hl=iw")
    except Exception:
        print("no")
    else:
        print("yes")

def main(): 
    #history()
    #ip()
    #folder_test()
    valid()
    s.p()
    
if __name__ == '__main__':
    main()

