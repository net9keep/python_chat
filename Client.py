# import socket
#
# SERVER_IP = "127.0.0.1"
# SERVER_PORT = 9002
# message = "hello"
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('127.0.0.1', 0))
# try:
#     sock.connect(('127.0.0.1', 20000))
#
#     send_buffer = bytes(message, encoding='utf-8')
#     sock.send(send_buffer)
#     print("나 : {0}".format(message))
#
#     recv_buffer = sock.recv(1024)
#     receive = str(recv_buffer, encoding='utf-8')
#     print("서버 : {0}".format(receive))
#
# finally:
#     sock.close()

import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 30001

s = socket.socket()
s.connect((SERVER_IP,SERVER_PORT))
s.send("hello".encode())
while True:
    print(s.recv(1024))
