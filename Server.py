import socket
import select

SERVER_IP = "127.0.0.1"
SERVER_PORT = 30001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP,SERVER_PORT))
s.listen(10)
input_list = [s]

while input_list:
    try:
        input_ready, write_ready, except_ready = select.select(input_list, [], [])

        for cl in input_ready:
            if cl == s:
                client, address = s.accept()
                #접속을 허가 했을때 표시할 내용
                print("new user join")
                input_list.append(client)
                for socket_in_list in input_list:
                    if socket_in_list != s and socket_in_list != cl:
                        try:
                            socket_in_list.send("new user join!")
                        except Exception as e:
                            socket_in_list.close()
                            input_list.remove(socket_in_list)
            else:
                data = cl.recv(1024)
                if data:
                    print("data is come", data)
                    for socket_in_list in input_list:
                        if socket_in_list != s and socket_in_list != cl:
                            try:
                                socket_in_list.send(data)
                            except Exception as e:
                                print(e)
                                socket_in_list.close()
                                input_list.remove(socket_in_list)
                                continue
                    cl.send(data)
                else:
                    cl.close()
                    input_list.remove(cl)
    except KeyboardInterrupt:
        s.close()

s.close()