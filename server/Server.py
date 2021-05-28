import socket,select,os,platform,getpass
import browserhistory as bh
import pandas as pd

MAX_MESSAGE_LENGTH = 1024
#names = pd.read_csv(r"D:\Python_Code_11\Access_Manager\database\names.csv")
#names = pd.read_csv("database\\names.csv")
names = pd.read_csv(os.path.join("database", "names.csv"))


def operating_system_starup():
    os_name = platform.system()
    if os_name == "Linux":
        os.system("sudo touch /lib/systemd/system/test-py.service")
        with open("/lib/systemd/system/test-py.service", "r+") as service:
            s = service.read()
            s.write("""[Unit]
            Description=Test Service
            After=multi-user.target
            Conflicts=getty@tty1.service

            [Service]
            Type=simple
            ExecStart=/usr/bin/python /home/boaz/Desktop/Programming/python/CyberProject/Server.py
            StandardInput=tty-force

            [Install]
            WantedBy=multi-user.target     
            """)
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl enable test-py.service")
        os.system("sudo systemctl start test-py.service")
    elif os_name == "Windows":
<<<<<<< HEAD:Server.py
        address = os.path.join("C:", "Users", getpass.getuser(), "AppData", "Roaming", "Microsoft",
                               "Windows", "Start Menu", "Programs, StartUp")  # TODO Change to exe later


=======
        bat_path = os.path.join("C:", "Users", getpass.getuser(),
                               "AppData", "Roaming", "Microsoft","Windows", "Start Menu", "Programs, StartUp")  # TODO Change to exe later
        file_path = os.path.dirname(os.path.realpath(__file__))
        #bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
            bat_file.write(r'start "" %s' % file_path)
            
>>>>>>> 6f3db6d0885921343dbfba5f0de513d60981236b:server/Server.py
class Server():  # TODO: ip working,make it exe,always on - turns on restart
    def __init__(self, port=8810):
        self.server_socket = socket.socket()
        self.server_socket.bind(("", port))
        self.server_socket.listen()
        print("[Server]: Server is up and running")

        self.open_client_sockets = []
        # [(self.current_socket, last data from client)]
        self.messages_to_send = []
        self.current_socket = None

        self.action = {"name": self.create_database, "history": self.history}
        self.customers_names = {}  # {socket.gethostname():current name}

    def get_requests(self):
        while True:
            self.rlist, self.wlist, self.xlist = select.select([self.server_socket] + self.open_client_sockets, self.open_client_sockets, [])

            self.receive()
            self.respond()

    def receive(self):
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
                    if data!="connection_available?":   
                        self.messages_to_send.append((self.current_socket, data))

    def respond(self):
        for message in self.messages_to_send:
            self.current_socket, data = message
            if self.current_socket in self.wlist:
                request = data.split("%")  # request[1]= name
                if request[0] == "name":
                    self.create_database(request[1])
                elif request[0] == "history":
                    self.history(request[1])
                else:
                    # can not run self.promblem beacuse it wiil get stuck
                    self.current_socket.send("[Error]: Unknown command".encode())
                self.messages_to_send.remove(message)

    def create_connection(self):
        connection, client_address = self.current_socket.accept()
        self.print_message("has joined!", client_address)
        self.open_client_sockets.append(connection)

    def create_database(self, name):  # add name to table
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
        try:
            history=pd.read_csv(f"history%{updated_name}.csv",engine="python",error_bad_lines=False,encoding='utf-8-sig')#encoding='utf-8-sig')#delim_whitespace=True
        except  Exception:
            #print("Exception")
            history=pd.read_csv(f"history%{updated_name}.csv",engine="python",error_bad_lines=False)     
        full_table=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        full_table["url"]=history[history.columns[0]]
        full_table["name"]=history[history.columns[1]]
        full_table["date"]=history[history.columns[2]]
        full_table["blocked"]="False"
        full_table["perm"]="False"
        full_table=full_table[full_table.date != "1601-01-01 02:00:00"]
        full_table.to_csv(os.path.join('database','customer',f"{updated_name}.csv"),index=False),#encoding='utf-8-sig')      

    def limitation(self,msg,url,start,end):
        if self.current_socket in self.wlist:
            self.current_socket.send(f"{msg}^^^{url}^^^{start}^^^{end}".encode())

    def print_message(self, message, client_address):  # to be deleted
        print(f"[{client_address}] {message}")

    def client_exit(self):
        self.print_message("has disconnected...",
                           self.current_socket.getpeername())
        self.open_client_sockets.remove(self.current_socket)
        self.current_socket.close()

    def close(self):
        self.server_socket.close()


def main():
    server = Server()
    server.get_requests()
    server.close()


if __name__ == "__main__":
    main()
