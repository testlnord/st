import json
import stserver_config
import urllib
from django.utils.http import urlquote

def addUser ( name, email):
    dict = {
        "name" : name,
        "email" :email
        }
    jsonData = json.dumps(dict)
    post_data = jsonData.encode("utf-8")
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/add_user"
    req = urllib.request.Request(url,post_data)
    response = urllib.request.urlopen(req)


def is_user_in_tour (name,t_name):
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)\
          +"/check_user_in_tour?name="+name+','+\
          't_name='+t_name
    response = urllib.request.urlopen(url)
    return dict(response)

def sendCreateTournament ( name, checker, timelimit, start_time, end_time):
    dict = {
        "name" : name,
        "checker" : str(checker),
        "timelimit":str(timelimit),
        "start_time" : str(start_time),
        "end_time" : str(end_time)
        }
    jsonData = json.dumps(dict)
    post_data = jsonData.encode("utf-8")
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/create_tournament"
    req = urllib.request.Request(url,post_data)
    response = urllib.request.urlopen(req)

def getUserInfoByName (name):
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_user_info?name="+name
    response = urllib.request.urlopen(url)
    return dict(response)

def get_run_result (runid):
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_run_result?runid="+str(runid)
    response = urllib.request.urlopen(url)
    return response

def get_user_tour_info (user_name):
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_user_tour_info?user_name="+user_name
    response = urllib.request.urlopen(url)
    return dict_list(response)


def run_tournament (t_name):
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/run_tournament?tournament_name="+t_name
    response = urllib.request.urlopen(url)
    return response

def dict (response):
    json_data= response.read().decode('utf-8')
    json_data=json.loads(json_data)
    if len(json_data)==1:
      json_data=json_data[0]
    return json_data

def dict_list (response):
    json_data= response.read().decode('utf-8')
    json_data=json.loads(json_data)
    return json_data


def add_user_to_tour (name,t_name):
    dict = {
        "name" : name,
        "tournament_name" : t_name
        }
    jsonData = json.dumps(dict)
    post_data = jsonData.encode("utf-8")
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/add_participant"
    req = urllib.request.Request(url,post_data)
    response = urllib.request.urlopen(req)




def send_solution (user_name,tournament_name,type,file):
    args="name="+user_name
    args+=","
    args+="tournament_name="+tournament_name
    args+=","
    args+="type="+type
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/send_solution?"+args

    post_data = file.read()
    req=urllib.request.Request(url,post_data)
    response = urllib.request.urlopen(req)
    return dict(response)

def get_tournaments ():
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_tournaments"
    response = urllib.request.urlopen(url)

    return dict_list(response)


def get_checkers ():
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_checkers"
    response = urllib.request.urlopen(url)
    return dict(response)

def get_builders ():
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_builders"
    response = urllib.request.urlopen(url)
    return dict(response)


def get_tour_results(tour):
    url = 'http://'+str(stserver_config.host)+':'+str(stserver_config.port)+"/get_run_result?tour_name="+urlquote(str(tour))
    response = urllib.request.urlopen(url)
    return dict(response)
