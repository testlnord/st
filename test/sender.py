from unittest.test.test_result import __init__

__author__ = 's'

import urllib.parse
import urllib.request
import json

class Sender:
    def  __init__(self,host,port):
        self.host = host
        self.port = port


    def sendUserInfo (self,name,email):
        dict = {
            "name" : name,
            "email" :email
            }
        jsonData = json.dumps(dict)
        post_data = jsonData.encode("utf-8")
        url = 'http://'+str(self.host)+':'+str(self.port)+"/add_user"
        req = urllib.request.Request(url,post_data)
        response = urllib.request.urlopen(req)




    def sendCreateTournament (self,name,checker,timelimit,start_time,end_time):
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


if __name__ == "__main__":
    s=Sender('127.0.0.1',8080)
    s.sendUserInfo('Vasya',"vasia@gmail.com")





