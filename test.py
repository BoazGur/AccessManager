import tkinter as tk
from tkinter import *
from tkinter import ttk
import socket,sys,os,time,pathlib,getpass,ctypes,glob
from urllib import request
import browserhistory as bh
import pandas as pd
from datetime import datetime as dt
import platform,platform,getpass,pathlib,shutil

Window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_hoster = Window_host
redirect = "127.0.0.1"
sites_to_block = ["www.one.co.il","instagram.com","www.instagram.com","www.walla.co.il","www.wikipedia.org"]


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

def ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(local_ip)


def folder_test():
    print(os.listdir("D:\Python_Code_11\Access_Manager\database"))


def is_valid_url(url):
    try:
        request.urlopen(url)
    except Exception:
        return False

    return True

        
def start():
    os_name = platform.system()
    if os_name == "Linux":
        os.system("crontab -e")
        os.system("@reboot python3 testUI.exe")

    elif os_name == "Windows":
        new_path =f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
        file_path ="D:\\Python_Code_11\\Access_Manager\\testUI.exe"

        if file_path==new_path:
            return
        else:
           #TODO change to exe
            #os.symlink(file_path,new_path)
            shutil.copyfile(file_path,new_path)         

def panda():
    full_table = pd.read_csv(os.path.join("database","customers","DESKTOP-OTB45S1","history.csv"))
    df_changes=pd.read_csv(os.path.join("database", "customers","DESKTOP-OTB45S1","changes.csv"))
    cols = list(full_table.columns)
    site="https://www.mako.co.il/"
    # row=full_table[full_table["url"]== "www.google.com"]
    # print(row)

    #print(bool(df_changes[df_changes["url"]== "https://stackoverflow.com/"].iloc[0][3]))
    # site="https://www.mako.co.il/,mako"
    # full_table.loc[full_table["url"]== site].iloc[0][3]=True


   
    #print(lst)
    #print(df_changes.url)
    #lst=df_changes.loc[df_changes.url==site,"url"].to_numpy().tolist()
    #full_table.loc[full_table.url.isin(lst), cols] = df_changes[df_changes["url"]== site].to_numpy().tolist()#TODO COPY PASTE
    #print(df_changes[df_changes["url"]== site].to_numpy().tolist())
    
   
   
    #full_table=full_table.apply(lambda  row : row["blocked"]==False if row["blocked"]!=True else None)
    full_table["blocked"]=full_table["blocked"].apply(lambda  row : False if row!=True else None)  #TODO COPY PASTE
    print(full_table)

def pd_index():
    #data = pd.read_csv(
        #os.path.join("database", "customers", "DESKTOP-OTB45S1.csv"))
    #print(type(data.loc[data.index == 1,"blocked"]))
    #print((data.loc[data.index == 1,"blocked"]).tolist()[0]==False)
    
    df_changes= pd.read_csv(os.path.join("database", "customers","DESKTOP-OTB45S1","changes.csv"))
    # df_changes.loc[df_changes["url"]== "https://stackoverflow.com/","blocked"]=False
    # print(df_changes)
    # #print(df_changes.loc[df_changes["url"]== "https://stackoverflow.com/","blocked"])
    # df_changes.to_csv(os.path.join("database", "customers","DESKTOP-OTB45S1","changes.csv"),index=False) 

    boolDf = df_changes.isin(["https://www.mako.co.il/"]).any().any()
    print(boolDf)
    
def add_row():
    df_changes= pd.read_csv(os.path.join("database", "customer","name1.csv"))
    new_row={"url":"1", "name":"2", "date":"12.4.21", "blocked":"True","perm":False, "start":1, "end":"23"}
    
    df_changes = df_changes.append(new_row, ignore_index=True)
    df_changes.to_csv(os.path.join("database", "customer","name1.csv"),index=False)
    
def paths(): 
    path = os.path.join("database", "customers")
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if 'history.csv' in file:
                files.append(os.path.join(r, file))
    for f in files:
        print(f)

def main():  
    history()
    #block_websites(0,23)
    #ip()
    #folder_test()
    #print(is_valid_url("https://www.w3schools.com/python/"))
    #pd_index()
    #panda()
    #paths()
    
    # df_changes= pd.read_csv(os.path.join("database", "customers","DESKTOP-OTB45S1","changes.csv"))
    # full_table = pd.read_csv(os.path.join("database","customers","DESKTOP-OTB45S1","history.csv"))
    # y=df_changes["url"].tolist()
    # lst=df_changes.loc[df_changes.url=="https://www.mako.co.il/","url"].to_numpy().tolist()
    # print(y)
    # print(lst)
    # cols = list(full_table.columns)
    
    # if lst[0] not in full_table["url"].tolist():
    #     full_table=full_table.append(df_changes.loc[df_changes.url=="https://www.morfix.co.il/",cols],ignore_index=True)
    #     full_table.to_csv(os.path.join("database","customers","DESKTOP-OTB45S1","history.csv"),index=False) 
   
if __name__ == '__main__':
    main()   

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False    

# if __name__ == '__main__':
#     if is_admin():
#         #pass
#         main()
#     else:
#         ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)#sys.argv[1:] if exe
#         main()