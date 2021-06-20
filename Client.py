import socket,time,platform,ctypes,sys
import browserhistory as bh
import platform
from datetime import datetime as dt



linux_host = '/etc/hosts'
window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_folder = ""
redirect = "127.0.0.1"
computer_name=socket.gethostname()

oran = "192.168.1.28"
amal_b = "10.30.57.83"

def operating_system():#TODO add startup capability
    """
    Find operating system to self.block_websites
    """
    global default_folder
    os_name = platform.system()
    if os_name == "Linux":
        default_folder = linux_host
    elif os_name == "Windows":
        default_folder = window_host    

class Client():  # TODO: ip working,make it exe,always on - turns on restart, all print() wiil be deleted
    def __init__(self, port=8810, ip=""):  # ip wiil change
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.bind(("", 37020))
        
        while True:
            data, addr = client.recvfrom(1024)
            if data:
                ip=addr[0]
                client.close()
                break
            
        self.s = socket.socket()
        self.port = port
        self.ip = ip
        while True:
            try:
                self.s.connect((self.ip,self.port))
                self.first_message()
            except Exception as e:
                print("waiting to server to come up")    
            else:
                break
        print("connected")
        self.sites_to_block=[]    #[[url1,start,end],[url2.start,end]]
              
    def run(self):
        """
        The main function of the class, calls to the other functions in the class
        """
        print("running")
        while True:
            self.block_websites()
            self.limitation()
            self.history()
                     
    def first_message(self):
        """
        send the name of the computer to the server
        """
        self.s.send(f"name%{computer_name}".encode())
        
    def limitation(self):
        """
        Recieve the limit message from the server and appends the variables to self.sites_to_block list
        """
        self.s.settimeout(0.2)
        message=""
        try:
            message=self.s.recv(1024).decode()
        except socket.error:
            pass
        else:
            print(f"message is {message}")
            request = message.split("^^^")
            if request[0]== "add url":
                if request[1][-1]=="/":
                        request[1]=request[1][0:-1]
                if request[1].startswith("www.",6,10):    
                    self.sites_to_block.append([request[1],request[2],request[3]])               
                else:
                    request[1]=request[1].split("//")[-1]# to add        
                    self.sites_to_block.append([request[1],int(request[2]),int(request[3])])           
            elif request[0]== "remove url":
                if request[1][-1]=="/":
                        request[1]=request[1][0:-1]
                if  not request[1].startswith("www.",6,10):
                    request[1]=request[1].split("//")[-1]
                # for site in self.sites_to_block:
                #     if site[0]==request[1]:
                #         site=[request[1],-1,-1]
                #         print("remove complete")
                for i in range(len(self.sites_to_block)):#remove url from host file
                    if self.sites_to_block[i][0]==request[1]:
                        self.sites_to_block[i]=[request[1],-1,-1]
                        print("remove complete")

    def history(self):
        """
        This function sends to the server the Internet browsing history
        """
        try:
            self.s.send(f"history%{computer_name}".encode())
        except Exception:
            self.try_connect()
        else:
            time.sleep(0.5)
            bh.get_browserhistory()   
            bh.write_browserhistory_csv()
            f = open("chrome_history.csv", "rb")
            l = f.read(1024)
            while (l):
                try:
                    self.s.send(l)
                except Exception:
                    self.try_connect()
                else:
                    l = f.read(1024)
            f.close()
     
                
    def block_websites(self):
        """
        The following function reads the hostfile and deaped on the time giving in UI it adds url or remove one. adding url 127.0.0.1 wiil redirects the url and  makes the site block
        """ 
        for websites in self.sites_to_block:
            if websites[1]==-1 and websites[2]==-1:
                with open(default_folder, 'r+') as hostfile:
                    hosts = hostfile.readlines()
                    hostfile.seek(0)
                    for host in hosts:
                        if not any(site in host for site in websites[0]):
                            hostfile.write(host)
                    hostfile.truncate()
                #print("Good Time...")
            else:    
                if dt(dt.now().year, dt.now().month, dt.now().day, websites[1]) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, websites[2]): # fuck off go to work        
                    with open(default_folder, 'r+') as hostfile:
                        hosts = hostfile.read()
                        if websites[0] not in hosts:
                            hostfile.write(redirect+' '+websites[0]+"\n")
                            print(f"block {websites[0]}")
                else:
                    with open(default_folder, 'r+') as hostfile:
                        hosts = hostfile.readlines()
                        hostfile.seek(0)
                        for host in hosts:
                            if not any(site in host for site in websites[0]):
                                hostfile.write(host)
                        hostfile.truncate()
                    print("Good Time...")
    
    def try_connect(self):
        """
        The  function will be called by others when s.send- makes an error(when srver if offline).The function will try to create a new connection and exit if succed to do so
        """
        self.s.close()
        self.s = socket.socket()
        print("waiting to server to come up") 
        while True:
            try:
                self.s.connect((self.ip,self.port))
                self.first_message()
            except Exception as e:
                pass   
            else:
                break
        time.sleep(2)
        self.run()
                
        
def main():
    operating_system()
    client = Client()
    client.run()

def is_admin():
    """
    chek if user is admin return true if runnig as administrator.
    """
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
