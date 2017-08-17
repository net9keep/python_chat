
from socket import *
from select import select
import Server_Info
import sys

SERVER_IP = Server_Info.SERVER_IP
SERVER_PORT = Server_Info.SERVER_PORT

def prompt():
    sys.stdout.write('<나> ')
    sys.stdout.flush()


client_socket = socket(AF_INET, SOCK_STREAM)
try:
    client_socket.connect((SERVER_IP,SERVER_PORT))
except Exception as e:
    print("서버에 접속하지 못했습니다.")

while True:
    try:
        connection_list = [sys.stdin, client_socket]
        input_ready, write_ready, except_ready = select(connection_list, [], [], 10)
        for sock in input_ready:
            if sock == client_socket:
                data = sock.recv(1024)
                if not data:
                    print("연결이...?")
                    prompt()
                else:
                    print(data)
                    prompt()
            else:
                message = sys.stdin.readline()
                client_socket.send(message.encode())
                prompt()
    except KeyboardInterrupt:
        client_socket.close()

