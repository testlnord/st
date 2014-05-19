#from unittest.test.test_result import __init__

__author__ = 's'

import urllib.parse
import urllib.request
import json
import zmq
import time



class Sender:
    def  __init__(self, host, port):
        self.host = host
        self.port = port

    def run_active_tour (self):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/run_active_tours"
        response = urllib.request.urlopen(url)
        return  response

    def get_run_result (self,tour_name):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/get_run_result?tour_name="+str(tour_name)
        response = urllib.request.urlopen(url)
        return response



    def sendUserInfo (self, name, email):
        dict = {
            "name" : name,
            "email" :email
            }
        jsonData = json.dumps(dict)
        post_data = jsonData.encode("utf-8")
        url = 'http://'+str(self.host)+':'+str(self.port)+"/add_user"
        req = urllib.request.Request(url)
        req.add_header('content-type',"application/json")
        response = urllib.request.urlopen(req,post_data)
        return response




    def sendCreateTournament (self, name, checker, timelimit, start_time, end_time):
        dict = {
            "name" : name,
            "checker" : str(checker),
            "timelimit":str(timelimit),
            "start_time" : str(start_time),
            "end_time" : str(end_time)
            }
        jsonData = json.dumps(dict)
        post_data = jsonData.encode("utf-8")
        url = 'http://'+str(self.host)+':'+str(self.port)+"/create_tournament"
        req = urllib.request.Request(url,post_data)
        response = urllib.request.urlopen(req)

    def getUserInfoByName (self,name):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/get_user_info?name="+name
        response = urllib.request.urlopen(url)
        return response



    def is_user_in_tour (self,name,t_name):
        url = 'http://'+str(self.host)+':'+str(self.port)\
              +"/check_user_in_tour?name="+name+','+\
              't_name='+t_name
        response = urllib.request.urlopen(url)
        return response


    def run_tournament (self,t_name):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/run_tournament?tournament_name="+t_name
        response = urllib.request.urlopen(url)
        return response

    def dict (self,response):
        json_data= response.read().decode('utf-8')
        json_data=json.loads(json_data)
        # if len(json_data)==1:
        #   json_data=json_data[0]
        return json_data

    def add_user_to_tour (self,name,t_name):
        dict = {
            "name" : name,
            "tournament_name" : t_name
            }
        jsonData = json.dumps(dict)
        post_data = jsonData.encode("utf-8")
        url = 'http://'+str(self.host)+':'+str(self.port)+"/add_participant"
        req = urllib.request.Request(url,post_data)
        response = urllib.request.urlopen(req)




    def send_solution (self,user_name,tournament_name,type,file_path):
        args="name="+user_name
        args+=","
        args+="tournament_name="+tournament_name
        args+=","
        args+="type="+type
        url = 'http://'+str(self.host)+':'+str(self.port)+"/send_solution?"+args
        f = open(file_path, 'r')
        post_data = f.read().encode('utf-8')
        req=urllib.request.Request(url,post_data)
        response = urllib.request.urlopen(req)

    def get_tournaments (self):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/get_tournaments"
        response = urllib.request.urlopen(url)
        return response


    def get_checkers (self):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/get_checkers"
        response = urllib.request.urlopen(url)
        return response
    def get_builders (self):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/get_builders"
        response = urllib.request.urlopen(url)
        return response


    def zmq_get_user_info_by_name (self,name):
        # self.id=1
        diction = {
            "key" : "get_user_info",
            "name" : name
            }
        return make_request(diction)
        # jsonData = json.dumps(diction)
        # context = zmq.Context()
        # socket = context.socket(zmq.DEALER)
        # identity = 'worker-%d' % self.id
        # socket.identity = identity.encode('utf-8')
        # socket.connect('tcp://localhost:8080')
        # print('Client %s started' % (identity))
        # poll = zmq.Poller()
        # poll.register(socket, zmq.POLLIN)
        # reqs = 0
        # socket.send_json(jsonData)
        # for i in range(5):
        #         sockets = dict(poll.poll(1000))
        #         if socket in sockets:
        #             msg = socket.recv_json()
        #             break
        # socket.close()
        # context.term()
        # return msg[0]


def make_request (dictionary):
    id = int(time.time()*1000)
    jsonData = json.dumps(dictionary)
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    identity = 'client-%d' % id
    socket.identity = identity.encode('utf-8')
    socket.connect('tcp://localhost:8080')
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)
    socket.send_json(jsonData)
    for i in range(5):
        sockets = dict(poll.poll(1000))
        if socket in sockets:
          msg = socket.recv_json()
          break
    socket.close()
    context.term()
    return msg[0]







if __name__ == "__main__":
    s=Sender('127.0.0.1',8080)
    # response=s.sendUserInfo("Kolyan","kolyan@ya.ru")
    # s.sendCreateTournament("test","tictactoe",10,123123,123124123)
    # s.add_user_to_tour("Kolyan5","test")
    # s.send_solution("Kolyan5","test","cpp","/home/s/python/NIR/st/test/tictactoe/cpp/main.cpp")

    #s.run_tournament("T1")
    # response = s.get_tournaments()
    # response = s.is_user_in_tour("Kolyan","test")
    # response = s.get_tournaments()

    # response = s.getUserInfoByName("Kolyan")
    print(s.zmq_get_user_info_by_name("Kolyan"))



