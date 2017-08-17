# import socketserver
#
# SERVER_IP = "127.0.0.1"
# SERVER_PORT = 10000
#
#
# class MyTCPHandler(socketserver.BaseRequestHandler):
#     def handler(self):
#         print("hello")
#         print(self.client_address[0])
#         sock = self.request
#
#         recv_buffer = sock.recv(1024)
#         receive = str(recv_buffer, encoding="utf-8")
#         print("receive : {0}".format(receive))
#
#         sock.send(receive)
#         sock.close()
#
#
# server = socketserver.TCPServer(('127.0.0.1', 20000), MyTCPHandler)
# print("Server Start")
# server.serve_forever()


import socket
import select

SERVER_IP = "127.0.0.1"
SERVER_PORT = 30001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP,SERVER_PORT))
s.listen()
input_list = [s]

while True:
    input_ready, write_ready, except_ready = select.select(input_list, [], [])

    for cl in input_ready:
        if cl == s:
            client, address = s.accept()
            #접속을 허가 했을때 표시할 내용
            print()
            input_list.append(client)
        else:
            data = cl.recv(1024)
            if data:
                print(data)
                cl.send(data)
            else:
                cl.close()
                input_list.remove(cl)

s.close()