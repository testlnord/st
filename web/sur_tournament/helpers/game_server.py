import json
import stserver_config
import urllib
from django.utils.http import urlquote
import time
import zmq
import base64


def make_request (dictionary):
    id = int(time.time()*1000)
    jsonData = json.dumps(dictionary)
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    identity = 'client-%d' % id
    socket.identity = identity.encode('utf-8')
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect('tcp://'+stserver_config.host +":"+stserver_config.port)
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)
    socket.send_json(jsonData)
    msg = None
    for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    msg = socket.recv_json()
                    break
    socket.close()
    context.term()
    print(msg)
    if not msg:
        return {}
    return msg



def addUser ( name, email):
    msg_dict = {
        "key" : "add_user",
        "name" : name,
        "email" :email
        }
    return make_request(msg_dict)


def is_user_in_tour (name,t_name):
    msg_dict = {
        "key" : "check_user_in_tour",
        "name" : name,
        "t_name" :t_name
        }
    return make_request(msg_dict)[0]

def sendCreateTournament ( name, checker, timelimit, start_time, end_time):
    msg_dict = {
        "key" : "create_tournament",
        "name" : name,
        "checker" : str(checker),
        "timelimit":str(timelimit),
        "start_time" : str(start_time),
        "end_time" : str(end_time)
        }
    return make_request(msg_dict)

def getUserInfoByName (name):
    msg_dict = {
        "key" : "get_user_info",
        "name" : name
    }

    return make_request(msg_dict)[0]

def get_run_result (runid):
    msg_dict = {
        "key" : "get_run_result",
        "runid" : runid
    }
    return make_request(msg_dict)

def get_user_tour_info (user_name):
    msg_dict = {
        "key" : "get_user_tour_info",
        "user_name" : user_name
    }
    return make_request(msg_dict)


def run_tournament (t_name):
    msg_dict = {
        "key" : "run_tournament",
        "tournament_name" : t_name
    }
    return make_request(msg_dict)


#def dict (response):
#    return response

#def dict_list (response):
#    json_data= response.read().decode('utf-8')
#    json_data=json.loads(json_data)
#    return json_data


def add_user_to_tour (name,t_name):
    msg_dict = {
        "key" : "add_participant",
        "name" : name,
        "tournament_name" : t_name
        }
    return make_request(msg_dict)




def send_solution (user_name,tournament_name,type,file):
     msg_dict = {
        "key" : "send_solution",
        "name" : user_name,
        "tournament_name" : tournament_name,
        "type" : type,
        "file" : base64.b64encode(file.read()).decode('utf-8')
        }
     return make_request(msg_dict)

def get_tournaments ():
    msg_dict = {
        "key" : "get_tournaments"
        }
    return make_request(msg_dict)

def get_checkers ():
    msg_dict = {
        "key" : "get_checkers"
        }
    return make_request(msg_dict)


def get_builders ():
    msg_dict = {
        "key" : "get_builders"
        }
    return make_request(msg_dict)


def get_tour_results(tour):
    msg_dict = {
        "key" : "get_run_result",
        "tour_name" : tour
        }
    return make_request(msg_dict)
