#server decorator
import os
import db
import util.register
import config


def supprort(method,key):
    def adder(handler):
        handler.supportedHandlers[key]=method
        return handler
    return adder


def make_out_path(tour_id, user_id):
    tour_path = os.path.join(config.out_path, str(tour_id))
    res_path = os.path.join(tour_path, str(user_id))
    return res_path

#DECORATORS
def addUser(db,data,path):
    name = data["name"]
    email= data["email"]
    db.addUser(name.email)


def getUserInfo(db,path):
    dict=parsePath(path)

    if "id" in dict:
        data=db.getUser(dict["id"])
    else:
        data=db.getUser(dict["name"])

    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")




def addTournament(db,data,path):
    name = data["name"]
    checker= data["checker"]
    timelimit = data["timelimit"]
    start_time = data ["start_time"]
    end_time  = data ["end_time"]
    db.addTournament(name,checker,timelimit,start_time,end_time)


def parsePath(path):
    s=path.split("?")[1]
    chunks=s.split(",")
    dict={}
    for chunk in chunks:
        key,value= chunk.split("=")
        dict[key]=value
    return dict

#madnes!!!
def wrapByComma (string):
    return "'"+string+"'"

def packArgs (args):
    s=""
    for arg in args:
        s+=","+str(arg)



