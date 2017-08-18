import socket
import select
import DataBase
import Server_Info
SERVER_IP = Server_Info.SERVER_IP
SERVER_PORT = Server_Info.SERVER_PORT
#ver 1

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((SERVER_IP,SERVER_PORT))
        self.s.listen(10)
        self.input_list = [self.s]
        self.listen()

    def check_data(self, data):
        #데이터 체크
        login_type = {"Login": "","SignUp": ""}
        data = data.decode()
        data_split = data.split()
        print(data_split)
        try:
            login_type['Login'] = data_split.index('Login')
        except ValueError:
            login_type['SignUp'] = 0

        if login_type['Login'] == 0 or login_type['SignUp'] == 0:
            id = data_split[1].replace("ID:","")
            pw = data_split[2].replace("PW:","")
            print("id:{0} pw:{1}".format(id,pw))
            chat_db = DataBase.DataBase()
            if login_type['Login'] == 0:
                chat_db.connect_db()
                result = chat_db.login(id, pw)
                if result:
                    return "login Success. welcome '" + id + "'!"
                else:
                    return "login False"
            elif login_type['SignUp'] == 0:
                # TODO write Database function call of SignUp
                chat_db.connect_db()
                result = chat_db.sign_up(id, pw)
                if result:
                    return "SignUp Success"
                else:
                    return "SignUp False"

        else:
            return data


    def listen(self):
        while self.input_list:
            try:
                input_ready, write_ready, except_ready = select.select(self.input_list, [], [])

                for cl in input_ready:
                    if cl == self.s:
                        client, address = self.s.accept()
                        #접속을 허가 했을때 표시할 내용
                        print("new user join")
                        self.input_list.append(client)
                        for socket_in_list in self.input_list:
                            if socket_in_list != self.s and socket_in_list != cl:
                                try:
                                    socket_in_list.send("new user join!".encode())
                                except Exception as e:
                                    socket_in_list.close()
                                    self.input_list.remove(socket_in_list)
                    else:
                        data = cl.recv(1024)
                        data = self.check_data(data)
                        if data:
                            print("data is come", data)
                            for socket_in_list in self.input_list:
                                if socket_in_list != self.s and socket_in_list != cl:
                                    try:
                                        print("send data", data)
                                        socket_in_list.send(data.encode())
                                    except Exception as e:
                                        print(e)
                                        socket_in_list.close()
                                        self.input_list.remove(socket_in_list)
                                        continue
                            cl.send(data.encode())
                        else:
                            cl.close()
                            self.input_list.remove(cl)
            except KeyboardInterrupt:
                self.s.close()
        self.s.close()

server = Server()
