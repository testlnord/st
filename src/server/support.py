#server decorator
import os
import db
import util.register
import config
import datetime


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




def addTournament(db, data, path):
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

def run(self, tour_name):
        tour_info = self.db.getTournament(name=tour_name)[0]
        tour_id = tour_info["id"]
        run_id = self.db.addRun(tour_id, str(datetime.datetime.now()))
        solutions = self.db.getSolutionsInTournament(tour_id)


        for sol1_num, sol1 in enumerate(solutions[:-1]):
            for sol2 in solutions[sol1_num + 1:]:
                r1 = util.register.runners[sol1["runner_name"]](
                    os.path.join(make_out_path(sol1["tour_id"], sol1["user_id"]), sol1["out_name"]),
                    tour_info["timeout"]
                )
                r2 = util.register.runners[sol2["runner_name"]](
                    os.path.join(make_out_path(sol2["tour_id"], sol2["user_id"]), sol2["out_name"]),
                    tour_info["timeout"]
                )
                #first time
                checker = util.register.checkers[tour_info["checker"]](r1, r2)
                checker.play()
                p1, p2 = checker.points()
                db.addGame(run_id, sol1["id"], sol2["id"], p1, p2, checker.log())
                #second time
                checker = util.register.checkers[tour_info["checker"]](r2, r1)
                checker.play()
                p1, p2 = checker.points()
                db.addGame(run_id, sol2["id"], sol1["id"], p1, p2, checker.log())

#madnes!!!
def wrapByComma (string):
    return "'"+string+"'"

def packArgs (args):
    s=""
    for arg in args:
        s+=","+str(arg)



