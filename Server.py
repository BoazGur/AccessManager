import socket,select,os
import pandas as pd

MAX_MESSAGE_LENGTH = 1024

path_names=os.path.join("database")
if not os.path.exists(path_names):
    os.makedirs(path_names)
    df_names=pd.DataFrame(columns=["name"])
    df_names.to_csv(os.path.join("database","names.csv"),index=False)
names = pd.read_csv(os.path.join("database", "names.csv"))

    
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
        self.blocked_url={}# current_socket:[blocked url] 
       
    def get_requests(self):
        """
        main function in the class,creation of rlist wlist xlist ,calls to self.receive() self.respond() that calls to other functions.
        """
        while True:
            self.rlist, self.wlist, self.xlist = select.select([self.server_socket] + self.open_client_sockets, self.open_client_sockets, [])

            self.receive()
            self.respond()

    def receive(self):
        """
        if socket try to connect receive creates the connection, 
        if socket already exists it receive the data and append the info to messages_to_send. The answer to data will be in respond function
        """
        for self.current_socket in self.rlist:
            if self.current_socket is self.server_socket:
                connection = self.create_connection()
                self.blocked_url[connection]=[]
            else:
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
                    print("send limit to client")
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
        self.print_message("has joined!", client_address)# to be deleted
        self.open_client_sockets.append(connection)
        return connection

    def create_database(self, name):  # add name to table
        """
        in charge of creating database that will store Internet browsing history of the client"
        """
        global names
        if name not in list(names["name"]):
            path=os.path.join("database", "customers",f"{name}")
            os.makedirs(path)
            
            names = names.append({"name": name}, ignore_index=True)
            names.to_csv(os.path.join("database", "names.csv"), index=False)

            df = pd.DataFrame(columns=["url", "name", "date", "blocked", "perm", "start", "end"])    
            df.to_csv(os.path.join("database", "customers",f"{name}","history.csv"), index=False)
            
            df_changes= pd.DataFrame(columns=["url", "name","date","blocked", "perm", "start", "end"])  
            df_changes.to_csv(os.path.join("database", "customers",f"{name}","changes.csv"), index=False)
        else:
            df_changes=pd.read_csv(os.path.join("database", "customers",f"{name}","changes.csv"))
            df_changes=df_changes[df_changes.blocked!="delete"]
            sites=df_changes["url"].tolist()
            for site in sites:
                if df_changes.loc[df_changes["url"]==site,"blocked"].any()==True:
                    start=df_changes.loc[df_changes["url"]==site,"start"]
                    end=df_changes.loc[df_changes["url"]==site,"end"]
                    self.limitation("add url", site, int(start), int(end))

    def history(self, name):  # must be admnstritor
        """
        The function reads the Internet browsing data that the client sent and store it in the database
        """
        path = os.path.join(f"history%{name}.csv")
        with open(path, 'wb') as f:
            while True:
                file = self.current_socket.recv(1024)
                if len(file) < 1024:
                    break
                f.write(file)
        f.close()
        
        history=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        history_full=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        try:
            history = pd.read_csv(f"history%{name}.csv",engine="python",error_bad_lines=False,encoding="utf-8-sig")#encoding='utf-8-sig')#delim_whitespace=True
        except pd.errors.EmptyDataError:
            history=history_full
        except UnicodeDecodeError:
            history = pd.read_csv(f"history%{name}.csv",engine="python",error_bad_lines=False)
                         
        full_table=pd.DataFrame(columns=["url","name","date","blocked","perm","start","end"])
        df_changes=pd.read_csv(os.path.join("database", "customers",f"{name}","changes.csv"))
        self.blocked_url[self.current_socket]=df_changes["url"].tolist()
            
        full_table["url"]=history[history.columns[0]]
        full_table["name"]=history[history.columns[1]]
        full_table["date"]=history[history.columns[2]]
        full_table["blocked"]=full_table["blocked"].apply(lambda  row : False if row!=True else None)  
        full_table["perm"]=full_table["perm"].fillna(False)
        full_table["start"]=full_table["start"].fillna(0)
        full_table["end"]=full_table["end"].fillna(0)

            
        cols = list(full_table.columns)
        for site in self.blocked_url[self.current_socket]: # update blocked value if url is blocked
            #df_changes=df_changes[df_changes.blocked!="delete"]#delet
            lst=df_changes.loc[df_changes.url==site,"url"].to_numpy().tolist()
            
            if len(df_changes["url"].tolist())>0:
                full_table.loc[full_table.url.isin(lst), cols] = df_changes[df_changes["url"]== site].to_numpy().tolist()

                if lst[0] not in full_table["url"].tolist():# add site
                    full_table=full_table.append(df_changes.loc[df_changes.url==site,cols],ignore_index=True)   
                           
            full_table=full_table[full_table.blocked!="delete"]
                
        full_table=full_table[full_table.date != "1601-01-01 02:00:00"]  
        df_changes.to_csv(os.path.join("database", "customers",f"{name}","changes.csv"),index=False)
        full_table.to_csv(os.path.join("database","customers",f"{name}","history.csv"),index=False)#encoding='utf-8-sig')      
        
    def limitation(self,msg,url,start,end):
        """
        This function send to client the info about the site that needs to be block
        """
        print("enter limitation function")
        self.blocked_url[self.current_socket].append(url)
        self.messages_to_send.append((self.current_socket, f"limit%{msg}^^^{url}^^^{start}^^^{end}"))

    def update_table(self,history,full_table,name):
        """
        The function update the history.csv in case of changes that the user makes
        Returns:[dataframe]: [updated table]
        """
        df_changes=pd.read_csv(os.path.join("database", "customers",f"{name}","changes.csv"))
        self.blocked_url[self.current_socket]=df_changes["url"].tolist()
        
        
        full_table["url"]=history[history.columns[0]]
        full_table["name"]=history[history.columns[1]]
        full_table["date"]=history[history.columns[2]]
        full_table["blocked"]=full_table["blocked"].apply(lambda  row : False if row!=True else None)  
        # full_table["perm"]=full_table["perm"].apply(lambda  row : False if row!=True else None)  
        
        
        cols = list(full_table.columns)
        for site in self.blocked_url[self.current_socket]: # update blocked value if url is blocked
            lst=df_changes.loc[df_changes.url==site,"url"].to_numpy().tolist()
            full_table.loc[full_table.url.isin(lst), cols] = df_changes[df_changes["url"]== site].to_numpy().tolist()
        return full_table
    
    
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
    

        

