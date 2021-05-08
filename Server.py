import socket
import select
import sqlite3

linux_host = '/etc/hosts'
window_host = r"C:\Windows\System32\drivers\etc\hosts"
default_folder = window_host
redirect = "127.0.0.1"


# To do :always on - turns on restart
class Server():
    def __init__(self, port=8810, ip="0.0.0.0"):
        self.server_soc = socket.socket()
        self.server_soc.bind((ip, port))
        self.server_soc.listen(1)

        self.action = {"exit": self.Exit}
        print("[Server]: Server is up and running")
        self.sites_to_block = ["www.facebook.com"]

    def get_requests(self):
        self.client_socket, self.client_address = self.server_soc.accept()
        print(f"[{self.client_address}] : Connected")
        while(True):
            message = self.client_socket.recv(1024).decode()
            self.action[message]()
            if message == "exit":
                break

    def exit(self):
        self.client_socket.send("Closing connection".encode())
        print(f"[{self.client_address}] Closing connection...")
        self.client_socket.close()

    def close(self):
        self.server_soc.close()




"""    def main_window(self):
        window = tk.Tk()

        #-------------------- Welcome Sign
        frame1 = tk.Frame(master=window, height=35 ,bg="red")
        frame1.pack(fill="both")

        fnt_welcome = tkFont.Font(size=35)
        lbl_welcome = tk.Label(master=frame1, text="Welcome Manager", font=fnt_welcome)
        lbl_welcome.pack()

        #-------------------- User Buttons
        frame2 = tk.Frame(master=window, width=100, bg="yellow")
        frame2.pack(fill="both", expand=True)



        window.geometry("800x700")
        window.mainloop()"""


def main():
    """server=Server()
    server.Get_requests()
    server.close()"""

    ui = ServerUI()
    ui.mainloop()


if __name__ == "__main__":
    main()
