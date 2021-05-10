import socket
import tkinter as tk
import tkinter.font as tkFont
import select

#To do :always on - turns on restart
class Server():
    def __init__(self, port=8810, ip="0.0.0.0"):
        self.server_soc = socket.socket()
        self.server_soc.bind((ip, port))
        self.server_soc.listen()
        print("[Server]: Server is up and running")
        
        self.open_client_sockets = []
        self.messages_to_send = [] # [(self.current_socket, last data from client, last data from server)]
        self.current_socket = None
        self.users={} #{self.current_socket: user1}
        self.start = {"sign_up": self.sign_up, "login": self.login}
        self.action = {"get_photo_names": self.get_photo_names, "download": self.download}
       
   
    def get_requests(self):
        pass

           

    def exit(self):
        self.client_socket.send("Closing connection".encode())
        print(f"[{self.client_address}] Closing connection...")
        self.client_socket.close()

    def close(self):
        self.server_soc.close()



def main():
    """server=Server()
    server.Get_requests()
    server.close()"""
    ui = ServerUI()
    ui.main_window()

if __name__=="__main__":
    main()
    
    
    
  
    

