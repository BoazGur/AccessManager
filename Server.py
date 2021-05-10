import socket
import select
from ServerUI import *
MAX_MESSAGE_LENGTH = 1024

class Server():#To do :always on - turns on restart
    def __init__(self, port=8810, ip="0.0.0.0"):
        self.server_soc = socket.socket()
        self.server_soc.bind((ip, port))
        self.server_soc.listen()
        print("[Server]: Server is up and running")
        
        self.open_client_sockets = []
        self.messages_to_send = [] # [(self.current_socket, last data from client, last data from server)]
        self.current_socket = None
        
        self.action = {"get_photo_names": self.get_photo_names, "download": self.download}
         
    def get_requests(self):
          while True:
            rlist, wlist, xlist = select.select([self.server_socket] + self.open_client_sockets, self.open_client_sockets, [])

            self.receive(rlist)
            self.respond(wlist)
    
    def receive(self,rlist):
        for self.current_socket in rlist:
            if self.current_socket is self.server_socket:
                connection = self.create_connection()
                self.messages_to_send.append((connection, opening_msg))
            else:
                print("Data from existing client")
                data = self.current_socket.recv(MAX_MESSAGE_LENGTH).decode()
                splited_data=data.split("%")
                if data == "exit":
                    self.exit()
                elif data[:6] == "upload":
                    self.upload(data)
                else:
                    self.messages_to_send.append((self.current_socket, data))
                    
    def respond(self,wlist):
        for message in self.messages_to_send :
            self.current_socket, data = message
            if self.current_socket in wlist:
                request = data.split("%")
                
                if data == opening_msg:
                    self.current_socket.send(opening_msg.encode())
                elif request[0] in self.start:
                    self.start[request[0]](request[1],request[2])
                elif data in self.action:
                    self.action[data]()
                elif request[0] in self.action:
                    self.action[request[0]](data)
                else:
                    self.current_socket.send("[Error]: Unknown command".encode())  # can not run self.promblem beacuse it wiil get stuck
                self.messages_to_send.remove(message)
                
           

    def create_connection(self):
        connection, client_address = self.current_socket.accept()
        self.print_message("has joined!", client_address)
        self.open_client_sockets.append(connection)
        
    def print_message(self, message, client_address):
        print(f"[{client_address}] {message}")

    def exit(self):
        self.print_message("has disconnected...",self.current_socket.getpeername())
        self.open_client_sockets.remove(self.current_socket)
        self.current_socket.close()

    def close(self):
        self.server_soc.close()



def main():
    """server=Server()
    server.Get_requests()
    server.close()"""

if __name__=="__main__":
    main()
    
    
    
  
    

