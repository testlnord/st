#server decorator
import os
import db
import util.register
import config
import json
import urllib.parse
import datetime

def support(method,key):
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
    data=get_dict_from_json_data(data)
    name = data["name"]
    email= data["email"]
    db.addUser(name,email)

def getUserInfo(db,path):
    dict=parsePath(path)

    if "id" in dict:
        print(dict["id"])
        data=db.getUser(dict["id"])
    else:
        print(dict["name"])
        data=db.getUser(None,dict["name"])

    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")

def addTournament(db,data,path):
    data=get_dict_from_json_data(data)
    name = data["name"]
    checker= data["checker"]
    timelimit = data["timelimit"]
    start_time = data ["start_time"]
    end_time  = data ["end_time"]
    db.addTournament(name,checker,timelimit,start_time,end_time)

def add_participant(db,data,path):
    data=get_dict_from_json_data(data)
    name = data["name"]
    t_name=data["tournament_name"]
    db.addParticipantByNames(t_name,name)


def add_solution (db,data,path):
    dict=parsePath(path)
    name=dict["name"]
    t_name=dict["tournament_name"]
    type=dict["type"]
    addBuild(db,name,t_name,data,type)



def run(db, tour_name):
        tour_info = db.getTournament(name=tour_name)[0]
        tour_id = tour_info["id"]
        run_id = db.addRun(tour_id, str(datetime.datetime.now()))
        solutions = db.getSolutionsInTournament(tour_id)

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


def addBuild(db, user_name, tour_name, file, builder):
    user_info = db.getUser(name=user_name)[0]
    tour_info = db.getTournament(name=tour_name)[0]
    o_path = make_out_path(tour_info["id"], user_info["id"])
    os.makedirs(o_path)
    builder = util.register.builders[builder]
    src_path = os.path.join(o_path, builder.def_src_name)
    with open(src_path, "w") as src_file:
        b = file.read(1).decode('utf-8')
        while b != "":
            src_file.write(b)
            b = file.read(1).decode('utf-8')
    b_stat = 0
    o_file = ""
    try:
        o_file = builder.build(src_path, o_path)
    except util.exceptions.BuildFailedException:
        b_stat = 1
    db.addSolution(user_info["id"], tour_info["id"], b_stat, str(datetime.datetime.now()), builder, o_file)

def parsePath(path):
    s=path.split("?")[1]
    chunks=s.split(",")
    dict={}
    for chunk in chunks:
        key,value= chunk.split("=")
        dict[key]=value
    return dict

def get_dict_from_json_data (json_post_data):
    post_data = urllib.parse.parse_qs(json_post_data.read().decode('utf-8'),keep_blank_values=1)
    json_data=next(iter(post_data.keys()))
    json_dict = json.loads(json_data)
    return json_dict






