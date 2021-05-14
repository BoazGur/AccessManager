import socket
import browserhistory as bh
from datetime import datetime as dt
import time

linux_host = '/etc/hosts'
window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_folder = window_host 
redirect = "127.0.0.1"

class Client():#To do :always on - turns on restart
    def __init__(self, port=8810, ip="0.0.0.0"):
        self.s = socket.socket()
        self.s.connect((ip,port))
        print("connected")# to be deleted     
    
    def first_message(self):
        self.s.send(f"name%{socket.gethostname()}".encode())
        
    def info(self):
        for line in open("my.csv"):
            self.s.send(line)
            
    def block_websites(self, start_hour , end_hour):
        while True:
            if dt(dt.now().year, dt.now().month, dt.now().day, start_hour) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, end_hour): # fuck off go to work
                print("Do the work ....")
                with open(default_folder, 'r+') as hostfile:
                    hosts = hostfile.read()
                    for site in self.sites_to_block:
                        if site not in hosts:
                            hostfile.write(redirect + ' ' + site + '\n')
            else:
                with open(default_folder, 'r+') as hostfile:
                    hosts = hostfile.readlines()
                    hostfile.seek(0)
                    for host in hosts:
                        if not any(site in host for site in self.sites_to_block):
                            hostfile.write(host)
                    hostfile.truncate()
                print("Good Time...")
            time.sleep(3)

def main():
   client = Client()
   client.first_message()
   client.info()
     
if __name__ == "__main__":
    main()