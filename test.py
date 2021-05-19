import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket,sys,os,re
import browserhistory as bh
from  urllib import  request
import urllib3
from Server import Server as s
import pandas as pd

df = pd.read_csv("database/customer/DESKTOP-OTB45S1.csv")

def host_name():
    print(socket.gethostname())

def history():
    #print(bh.get_browserhistory())
    # dict_obj = bh.get_browserhistory()
    # print(dict_obj.keys())
   
    bh.write_browserhistory_csv()
    history=pd.read_csv(os.path.join(f"chrome_history.csv"),engine="python",encoding='',error_bad_lines=False)
    
    print(history.info())
    #file=open("Browserhistory.csv")
    
    #print(bh.get_database_paths())
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
def lst():
    lst=[]
    a=["banana","x",8]
    b=["car",10,11]
    lst.append(a)
    lst.append(b)
    print(lst)
    print(lst[1])
def table():
    table=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
    df=pd.read_csv("history.csv")
    full_table= pd.concat([table,df])
    print(full_table)
    
def main():  
    history()
    #ip()
    #folder_test()
    #valid()
    #table()

    
if __name__ == '__main__':
    main()

