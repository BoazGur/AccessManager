import socket,select,os
import browserhistory as bh
import pandas as pd
#from ServerUI import *

MAX_MESSAGE_LENGTH = 1024
#names = pd.read_csv(r"D:\Python_Code_11\Access_Manager\database\names.csv")
#names = pd.read_csv("database\\names.csv")
names = pd.read_csv(os.path.join("database","names.csv"))

class Server():#TODO: ip working,make it exe,always on - turns on restart
    def __init__(self, port=8810):
        self.server_socket = socket.socket()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.server_socket.bind((local_ip, port))
        self.server_socket.listen()
        print("[Server]: Server is up and running")
        
        self.open_client_sockets = []
        self.messages_to_send = [] # [(self.current_socket, last data from client)]
        self.current_socket = None
        
        self.action = {"history": self.history}
         
    def get_requests(self):
          while True:
            self.rlist, self.wlist, self.xlist = select.select([self.server_socket] + self.open_client_sockets, self.open_client_sockets, [])

            self.receive()
            self.respond()
    
    def receive(self):
        for self.current_socket in self.rlist:
            if self.current_socket is self.server_socket:
                connection = self.create_connection()
                self.messages_to_send.append((connection,""))
            else:
                print("Data from existing client")
                data = self.current_socket.recv(MAX_MESSAGE_LENGTH).decode()
                if data == "exit":
                    self.exit()
                else:
                    self.messages_to_send.append((self.current_socket, data))
                    
    def respond(self):
        for message in self.messages_to_send :
            self.current_socket, data = message
            if self.current_socket in self.wlist:
                request = data.split("%")
                if request[0]=="name":# add name to table
                    self.create_database(request)
                elif data=="history":
                    self.history()
                else:                   
                    self.current_socket.send("[Error]: Unknown command".encode())  # can not run self.promblem beacuse it wiil get stuck
                self.messages_to_send.remove(message)
    
    def create_connection(self):
        connection, client_address = self.current_socket.accept()
        self.print_message("has joined!", client_address)
        self.open_client_sockets.append(connection)
    
    def create_database(self,request):  
        global names
        if request[1] not in list(names["name"]):
            names=names.append({"name":request[1]},ignore_index=True)
            names.to_csv(os.path.join("database","names.csv"),index=False)
        
        df=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        df.to_csv(os.path.join('database','customer',f"{request[1]}.csv"), index=False)
            
    def history(self):
        path=os.path.join("history.csv")
        with open(path, 'wb') as f:
            while True:
                file = self.current_socket.recv(1024)
                if len(file) < 1024:
                    break                 
                f.write(file)
        f.close()
        print("succesfuly upload history")
       
    def limitation(self,msg,url,start,end):
        if self.current_socket in self.wlist:
            self.current_socket.send(f"{msg}%{url}%{start}%{end}".encode())
    
    
    
    def print_message(self, message, client_address):# to be deleted
        print(f"[{client_address}] {message}")

    def exit(self):
        self.print_message("has disconnected...",self.current_socket.getpeername())
        self.open_client_sockets.remove(self.current_socket)
        self.current_socket.close()

    def close(self):
        self.server_socket.close()
    
def main():
    server=Server()
    server.get_requests()
    server.close()

if __name__=="__main__":
    main()
    
    
    
  
    

