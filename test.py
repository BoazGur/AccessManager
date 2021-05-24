import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket
import sys
import os
import re
import browserhistory as bh
from urllib import request
import urllib3
#from Server import Server as s
import pandas as pd
from datetime import datetime as dt
import time

Window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_hoster = Window_host
redirect = "127.0.0.1"
sites_to_block = ["www.one.co.il","www.instagram.com"]


df = pd.read_csv("database/customer/DESKTOP-OTB45S1.csv")
names = pd.read_csv(os.path.join("database", "names.csv"))


def host_name():
    print(socket.gethostname())


def history():
    # print(bh.get_browserhistory())
    # dict_obj = bh.get_browserhistory()
    # print(dict_obj.keys())

    bh.write_browserhistory_csv()
    history = pd.read_csv(os.path.join(f"chrome_history.csv"),
                          engine="python", encoding='', error_bad_lines=False)

    print(history.info())
    # file=open("Browserhistory.csv")

    # print(bh.get_database_paths())
    # print(bh.get_username())


def ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)


def folder_test():
    print(os.listdir("D:\Python_Code_11\Access_Manager\database"))


def valid():
    resp = None
    try:
        resp = request.urlopen("https://www.google.co.il/?hl=iw")
    except Exception:
        print("no")
    else:
        print("yes")


def lst():
    lst = []
    a = ["banana", "x", 8]
    b = ["car", 10, 11]
    lst.append(a)
    lst.append(b)
    print(lst)
    print(lst[1])


def table():
    table = pd.DataFrame(
        columns=["url", "name", "date", "blocked", "perm", "start", "end"])
    df = pd.read_csv("history.csv")
    full_table = pd.concat([table, df])
    print(full_table)

def block_websites(start_hour , end_hour):
    while True:
        if dt(dt.now().year, dt.now().month, dt.now().day,start_hour)< dt.now() < dt(dt.now().year, dt.now().month, dt.now().day,end_hour): 
            print("Do the work ....")
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.read()
                for site in  sites_to_block:
                    if site not in hosts:
                       hostfile.write(redirect+' '+site+'\n')
        else:
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.readlines()
                hostfile.seek(0)
                for host in hosts:
                    if not any(site in host for site in sites_to_block):
                        hostfile.write(host)
                hostfile.truncate()
            print('Good Time')
        time.sleep(3)
def main():  
    #history()
    #ip()
    #folder_test()
    #valid()
    #table()
    block_websites(0,23)
    
if __name__ == '__main__':
    main()
