import socket,select,os,platform,getpass
import pandas as pd

MAX_MESSAGE_LENGTH = 1024
#names = pd.read_csv(r"D:\Python_Code_11\Access_Manager\database\names.csv")
#names = pd.read_csv("database\\names.csv")
names = pd.read_csv(os.path.join("database", "names.csv"))

def operating_system_starup():
    os_name = platform.system()
    if os_name == "Linux":
        pass
        # os.system("sudo touch /lib/systemd/system/test-py.service")
        # with open("/lib/systemd/system/test-py.service", "r+") as service:
        #     s = service.read()
        #     s.write("""[Unit]
        #     Description=Test Service
        #     After=multi-user.target
        #     Conflicts=getty@tty1.service

        #     [Service]
        #     Type=simple
        #     ExecStart=/usr/bin/python /home/boaz/Desktop/Programming/python/CyberProject/Server.py
        #     StandardInput=tty-force

        #     [Install]
        #     WantedBy=multi-user.target     
        #     """)
        # os.system("sudo systemctl daemon-reload")
        # os.system("sudo systemctl enable test-py.service")
        # os.system("sudo systemctl start test-py.service")
    elif os_name == "Windows":
        pass
    
class Server():  # TODO: ip working,make it exe,always on - turns on restart
    def __init__(self, port=8810):
        """
        creation of server_socket and establish self.variables
        """
        self.server_socket = socket.socket()
        self.server_socket.bind(("", port))
        self.server_socket.listen()
        print("[Server]: Server is up and running")

        self.open_client_sockets = []
        self.messages_to_send = [] # [(self.current_socket, last data from client)]
        self.current_socket = None

        self.action = {"name": self.create_database, "history": self.history}
        self.customers_names = {}  # {socket.gethostname():current name}

    def get_requests(self):
        """
        main function in the class,creation of rlist wlist xlist ,calls to self.receive() self.respond() that call to other functions.
        """
        while True:
            self.rlist, self.wlist, self.xlist = select.select([self.server_socket] + self.open_client_sockets, self.open_client_sockets, [])

            self.receive()
            self.respond()

    def receive(self):
        """
        if socket try to connect receive create connection, 
        if socket already exists it receive the data and append the info to messages_to_send the answer to data will be in respond function
        """
        for self.current_socket in self.rlist:
            if self.current_socket is self.server_socket:
                connection = self.create_connection()
                self.messages_to_send.append((connection, ""))
            else:
                print("Data from existing client")
                data=""
                try:
                    data = self.current_socket.recv(MAX_MESSAGE_LENGTH).decode()
                except Exception:
                    self.client_exit()
                else: 
                    self.messages_to_send.append((self.current_socket, data))

    def respond(self):
        """
        This function responsible to call other functions acording to data
        """
        for message in self.messages_to_send:
            self.current_socket, data = message
            if self.current_socket in self.wlist:
                request = data.split("%")  # request[1]= name
                if request[0] == "name":
                    self.create_database(request[1])  
                elif request[0] == "history":
                    self.history(request[1])
                elif request[0]=="limit":
                    self.current_socket.send(request[1].encode())
                else:
                    # can not run self.promblem beacuse it wiil get stuck
                    self.current_socket.send("[Error]: Unknown command".encode())
                self.messages_to_send.remove(message)

    def create_connection(self):
        """
        create connection between server and client
        """
        connection, client_address = self.current_socket.accept()
        self.print_message("has joined!", client_address)
        self.open_client_sockets.append(connection)

    def create_database(self, name):  # add name to table
        """
        in charge of creating database that will store Internet browsing history of the client"
        """
        global names
        self.customers_names[name] = ""

        if name not in list(names["name"]):
            names = names.append({"name": name}, ignore_index=True)
            names.to_csv(os.path.join("database", "names.csv"), index=False)

        df = pd.DataFrame(
            columns=["url", "name", "date", "blocked", "perm", "start", "end"])
        # PermissionError: [Errno 13] Permission denied: if file is open
        df.to_csv(os.path.join('database', 'customer',
                               f"{name}.csv"), index=False)

    def history(self, name):  # must be admnstritor
        """
        The function reads the Internet browsing data that the client sent and store it in the database
        """
        updated_name = name
        if self.customers_names[name] != "":
            updated_name = self.customers_names[name]

        path = os.path.join(f"history%{updated_name}.csv")
        with open(path, 'wb') as f:
            while True:
                file = self.current_socket.recv(1024)
                if len(file) < 1024:
                    break
                f.write(file)
        f.close()
        
        history_full=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        history=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        try:
            history = pd.read_csv(f"history%{updated_name}.csv",engine="python",error_bad_lines=False,encoding='utf-8-sig')#encoding='utf-8-sig')#delim_whitespace=True
        except pd.errors.EmptyDataError:
            history=history_full
                         
        full_table=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        full_table["url"]=history[history.columns[0]]
        full_table["name"]=history[history.columns[1]]
        full_table["date"]=history[history.columns[2]]
        full_table["blocked"]="False"
        full_table["perm"]="False"
        full_table=full_table[full_table.date != "1601-01-01 02:00:00"]
        full_table.to_csv(os.path.join('database','customer',f"{updated_name}.csv"),index=False),#encoding='utf-8-sig')      

    def limitation(self,msg,url,start,end):
        """
        This function send to client the info about the site that needs to be block
        """
        print("enter limitation function ")
        self.messages_to_send.append(((self.current_socket, f"limit%{msg}^^^{url}^^^{start}^^^{end}")))
        
        # if self.current_socket in self.wlist:
        #     self.current_socket.send(f"{msg}^^^{url}^^^{start}^^^{end}".encode())
        #     print(f"{msg}^^^{url}^^^{start}^^^{end} noder")
    
    
    def print_message(self, message, client_address):  # to be deleted
        print(f"[{client_address}] {message}")

    def client_exit(self):
        """
        The function will be called when the connection ends  
        """
        self.print_message("has disconnected...",
                           self.current_socket.getpeername())
        self.open_client_sockets.remove(self.current_socket)
        
        self.current_socket.close()


