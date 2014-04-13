#from unittest.test.test_result import __init__

__author__ = 's'

import urllib.parse
import urllib.request
import json

class Sender:
    def  __init__(self, host, port):
        self.host = host
        self.port = port


    def sendUserInfo (self, name, email):
        dict = {
            "name" : name,
            "email" :email
            }
        jsonData = json.dumps(dict)
        post_data = jsonData.encode("utf-8")
        url = 'http://'+str(self.host)+':'+str(self.port)+"/add_user"
        req = urllib.request.Request(url,post_data)
        response = urllib.request.urlopen(req)




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
        return

    def get_run_result (self,run_name):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/get_run_result?runid=5"
        response = urllib.request.urlopen(url)
        return response

    def run_tournament (self,t_name):
        url = 'http://'+str(self.host)+':'+str(self.port)+"/run_tournament?tournament_name="+t_name
        response = urllib.request.urlopen(url)
        return response

    def dict (self,response):
        json_data= response.read().decode('utf-8')
        json_data=json.loads(json_data)
        json_data=json_data[0]
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





if __name__ == "__main__":
    s=Sender('127.0.0.1',8080)
    s.sendUserInfo("Kolyan2","kolyan@ya.ru")
    # s.sendCreateTournament("test5","tictactoe",10,123123,123124123)
    # s.add_user_to_tour("Kolyan2","test5")
    # s.send_solution("Kolyan","test5","cpp","/home/s/PycharmProjects/st/test/tictactoe/cpp/main.cpp")
    # response = s.getUserInfoByName('Barybasyan')
    # print(s.dict(response))

    # s.run_tournament("test5")
    response = s.get_run_result("blabl")
    print(s.dict(response))





