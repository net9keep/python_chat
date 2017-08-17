
from socket import *
from select import select
import Server_Info
import sys

SERVER_IP = Server_Info.SERVER_IP
SERVER_PORT = Server_Info.SERVER_PORT


class Client:

    def __init__(self):
        self.id = self.pw = ""
        self.data = {}
        self.choice = 0
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
        except Exception as e:
            print("서버에 접속하지 못했습니다.")
            sys.exit()
        print("서버에 접속했습니다")
        self.login()

    def login(self):
        print("*--------------*")
        print("1.login")
        print("2.SignUp")
        print("*--------------*")
        self.choice = input("> ")
        print(self.choice)
        if self.choice == '1':
            print("*--------------*")
            self.id = input("id > ")
            self.pw = input("pw > ")
            print("*--------------*")
        elif self.choice == '2':
            print("*----signup----*")
            self.id = input("id > ")
            self.pw = input("pw > ")
            print("*--------------*")
        else:
            print("wrong number")
            self.login()
        self.data = {"id": self.id, "pw": self.pw}
        self.send_data()

    def send_data(self):
        while True:
            try:
                connection_list = [sys.stdin, self.client_socket]
                input_ready, write_ready, except_ready = select(connection_list, [], [], 10)
                for sock in input_ready:
                    if sock == self.client_socket:
                        data = sock.recv(1024)
                        if not data:
                            print("연결이...?")
                            self.prompt()
                        elif data == "SignUp Success":
                            print(data)
                            self.prompt()
                        else:
                            print(data)
                            self.prompt()
                            if self.data and self.choice == '1':
                                message = "Login ID:{0} PW:{1}".format(self.data["id"], self.data["pw"]).encode()
                                self.client_socket.send(message)
                                self.choice = 0
                            elif self.data and self.choice == '2':
                                message = "SignUp ID:{0} PW:{1}".format(self.data["id"], self.data["pw"]).encode()
                                self.client_socket.send(message)
                                self.choice = 0
                    else:
                        message = sys.stdin.readline()
                        self.client_socket.send(message.encode())
                        self.prompt()
            except KeyboardInterrupt:
                self.client_socket.close()

    def prompt(self):
        sys.stdout.write('<나> ')
        sys.stdout.flush()

client = Client()
