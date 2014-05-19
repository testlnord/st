import json
import stserver_config
import urllib
from django.utils.http import urlquote
import time
import zmq



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
    msg = None
    #for i in range(10):
    #    sockets = dict(poll.poll(1000))
    #    if socket in sockets:
    #      print("socked recived")
    #      msg = socket.recv_json()
    #      break
    msg = socket.recv_json()
    socket.close()
    context.term()
    print(msg)
    if not msg:
        return {}
    return msg



def addUser ( name, email):
    dict = {
        "key" : "add_user",
        "name" : name,
        "email" :email
        }
    # jsonData = json.dumps(dict)
    # post_data = jsonData.encode("utf-8")
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/add_user"
    # req = urllib.request.Request(url,post_data)
    # response = urllib.request.urlopen(req)
    return make_request(dict)


def is_user_in_tour (name,t_name):
    dict = {
        "key" : "check_user_in_tour",
        "name" : name,
        "t_name" :t_name
        }
    return make_request(dict)
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)\
    #       +"/check_user_in_tour?name="+name+','+\
    #       't_name='+t_name
    # response = urllib.request.urlopen(url)
    # return dict(response)

def sendCreateTournament ( name, checker, timelimit, start_time, end_time):
    dict = {
        "key" : "create_tournament",
        "name" : name,
        "checker" : str(checker),
        "timelimit":str(timelimit),
        "start_time" : str(start_time),
        "end_time" : str(end_time)
        }
    return make_request(dict)
    # jsonData = json.dumps(dict)
    # post_data = jsonData.encode("utf-8")
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/create_tournament"
    # req = urllib.request.Request(url,post_data)
    # response = urllib.request.urlopen(req)

def getUserInfoByName (name):
    dict = {
        "key" : "get_user_info",
        "name" : name
    }
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_user_info?name="+name
    # response = urllib.request.urlopen(url)
    # return dict(response)
    return make_request(dict)[0]

def get_run_result (runid):
    dict = {
        "key" : "get_run_result",
        "runid" : runid
    }
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_run_result?runid="+str(runid)
    # response = urllib.request.urlopen(url)
    # return response
    return make_request(dict)

def get_user_tour_info (user_name):
    dict = {
        "key" : "get_user_tour_info",
        "user_name" : user_name
    }
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_user_tour_info?user_name="+user_name
    # response = urllib.request.urlopen(url)
    # return dict_list(response)
    return make_request(dict)


def run_tournament (t_name):
    dict = {
        "key" : "run_tournament",
        "tournament_name" : t_name
    }
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/run_tournament?tournament_name="+t_name
    # response = urllib.request.urlopen(url)
    # return response
    return make_request(dict)


def dict (response):
    return response
    #json_data= response.read().decode('utf-8')
    #json_data=json.loads(json_data)
    #if len(json_data)==1:
    #  json_data=json_data[0]
    #return json_data

def dict_list (response):
    json_data= response.read().decode('utf-8')
    json_data=json.loads(json_data)
    return json_data


def add_user_to_tour (name,t_name):
    dict = {
        "key" : "add_participant",
        "name" : name,
        "tournament_name" : t_name
        }
    # jsonData = json.dumps(dict)
    # post_data = jsonData.encode("utf-8")
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/add_participant"
    # req = urllib.request.Request(url,post_data)
    # response = urllib.request.urlopen(req)
    return make_request(dict)




def send_solution (user_name,tournament_name,type,file):
     dict = {
        "key" : "send_solution",
        "name" : user_name,
        "tournament_name" : tournament_name,
        "type=" : type,
        "file=" : file.read()
        }
    # args="name="+user_name
    # args+=","
    # args+="tournament_name="+tournament_name
    # args+=","
    # args+="type="+type
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/send_solution?"+args
    #
    # post_data = file.read()
    # req=urllib.request.Request(url,post_data)
    # response = urllib.request.urlopen(req)
    # return dict(response)
     return make_request(dict)

def get_tournaments ():
    dict = {
        "key" : "get_tournaments"
        }
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_tournaments"
    # response = urllib.request.urlopen(url)
    #
    # return dict_list(response)
    return make_request(dict)

def get_checkers ():
    dict = {
        "key" : "get_checkers"
        }
    return make_request(dict)
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_checkers"
    # response = urllib.request.urlopen(url)
    # return dict(response)


def get_builders ():
    dict = {
        "key" : "get_builders"
        }
    return make_request(dict)
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_builders"
    # response = urllib.request.urlopen(url)
    # return dict(response)


def get_tour_results(tour):
    dict = {
        "key" : "get_run_result",
        "tour_name" : tour
        }
    return make_request(dict)
    # url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_run_result?tour_name="+urlquote(str(tour))
    # response = urllib.request.urlopen(url)
    # return dict(response)
