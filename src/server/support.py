#server decorator
import base64
from lib2to3.patcomp import _type_of_literal
import os
import db
import util.register
import config
import json
import urllib.parse
import datetime
import time
import sqlite3


supportedHandlers = {}


def jsonify(data):
    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")


def support(key):
    def adder(method):
        supportedHandlers[key] = method
        return method

    return adder


def date2db(date):
    a = date.strftime("%Y-%m-%d %H:%M:%S.000000")
    return a



def make_out_path(tour_id, user_id, time_salt=None):
    tour_path = os.path.join(config.out_path, str(tour_id))
    res_path = os.path.join(tour_path, str(user_id))
    #adding send time mark
    if time_salt is None:
        time_salt = str(time.time())
    res_path = os.path.join(res_path, time_salt)
    return res_path


def make_runner(sollution, timelimit):
    r = util.register.runners[sollution["runner_name"]](
        os.path.join(make_out_path(sollution["tour_id"], sollution["user_id"],sollution["time"]), sollution["file_name"]),
        timelimit)

    return r


#DECORATORS
@support("add_user")
def addUser(db, data):
    name = data["name"]
    email = data["email"]

    db.addUser(name, email)
    dict = ["user " + name + " added"]
    return jsonify(dict)


@support("get_user_info")
def getUserInfo(db, data):

    if "id" in data:
        data = db.getUser(data["id"])
    else:
        data = db.getUser(None, data["name"])
    return jsonify(data)


@support("get_tournaments")
def get_tournaments(db, data):
    data = db.getTournament()
    return jsonify(data)


@support("get_checkers")
def get_checkers(db, data):
    data = list(util.register.checkers.keys())
    print(data)
    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")


@support("get_builders")
def get_builders(db, data):
    data = list(util.register.builders.keys())
    print(data)
    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")


@support("create_tournament")
def addTournament(db, data):
    name = data["name"]
    checker = data["checker"]
    timelimit = data["timelimit"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    db.addTournament(name, checker, timelimit, start_time, end_time)


@support("add_participant")
def add_participant(db, data):
    if not data:
        return
    name = data["name"]
    t_name = data["tournament_name"]
    db.addParticipantByNames(t_name, name)


@support("send_solution")
def add_solution(db, dict):
   name = dict["name"]
   t_name = dict["tournament_name"]
   type = dict["type"]
   file = base64.b64decode(bytes(dict["file"], 'utf-8'))
   return jsonify(addBuild(db, name, t_name, file, type))


@support("run_tournament")
def run_tournament(db, data):
    tour_name = data["tournament_name"]
    tour_info = db.getTournament(name=tour_name)[0]
    run_by_tinfo(db, tour_info)
    return None


@support("get_run_result")
def get_run_result(db, data):
    data = db.getRunResult(data["tour_name"])
    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")


@support("get_user_tour_info")
def get_run_result(db, data):
    data = db.getUserTours(data["user_name"])
    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")


@support("check_user_in_tour")
def checkUserInTournament(db, data):
    data = db.checkUserInTour(data['name'], data['t_name'])
    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")


@support("get_game_log")
def getGameLog(db, data):
    data = db.getGameLog(data['game_id'])
    jsonData = json.dumps(data)
    return jsonData.encode("utf-8")


@support("run_active_tours")
def run_active_tours(db, data):
    tinfos = db.get_active_tours()
    for t in tinfos:
        print("run ", t)
        run_by_tinfo(db, t)


def run_by_tinfo(db, tinfo):
    tid = tinfo["id"]
    timelimit = tinfo["tl"]
    run_id = db.addRun(tid, date2db(datetime.datetime.now()))
    solutions = db.getSolutionsInTournament(tid)

    for sol1_num, sol1 in enumerate(solutions[:-1]):
        for sol2 in solutions[sol1_num + 1:]:
            r1 = make_runner(sol1, timelimit)
            r2 = make_runner(sol2, timelimit)

            #first time
            checker = util.register.checkers[tinfo["c"]](r1, r2)
            checker.play()
            p1, p2 = checker.points()
            print(p1, p2)
            db.addGame(run_id, sol1["id"], sol2["id"], p1, p2, checker.log())
            #second time
            checker = util.register.checkers[tinfo["c"]](r2, r1)
            checker.play()
            p1, p2 = checker.points()
            print(p1, p2)
            db.addGame(run_id, sol2["id"], sol1["id"], p1, p2, checker.log())


def create_run(db, tour_name):
    tour_info = db.getTournament(name=tour_name)[0]
    tour_id = tour_info["id"]

    run_id = db.addRun(tour_id, date2db(datetime.datetime.now()))
    solutions = db.getSolutionsInTournament(tour_id)

    for sol1_num, sol1 in enumerate(solutions[:-1]):
        for sol2 in solutions[sol1_num + 1:]:
            db.addGame(run_id, sol2["id"], sol1["id"], 0, 0, 'NOT PLAYED')


def addBuild(db, user_name, tour_name, file, builder_name):
    result = {"ok": True, "msg": ''}
    cur_time = time.time()
    user_info = db.getUser(name=user_name)[0]
    tour_info = db.getTournament(name=tour_name)[0]
    o_path = make_out_path(tour_info["id"], user_info["id"], str(cur_time))
    os.makedirs(o_path)
    builder = util.register.builders[builder_name]
    src_path = os.path.join(o_path, builder.def_src_name)

    fileparams = 'w'
    if type(file) == bytes:
        fileparams += 'b'
    with open(src_path, fileparams) as src_file:
        src_file.write(file)
    b_stat = 0
    o_file = ""
    try:
        o_file = builder.build(src_path, o_path)
    except util.exceptions.BuildFailedException as e:
        b_stat = 1
        result["ok"] = False
        result["msg"] = str(e)

    db.addSolution(user_info["id"], tour_info["id"], b_stat, str(cur_time), builder_name, o_file)
    return result


def parsePath(path):
    s = path.split("?")[1]
    chunks = s.split(",")
    dict = {}
    for chunk in chunks:
        key, value = chunk.split("=")
        dict[key] = value
    return dict


def get_dict_from_json_data(json_post_data):
    # return json_post_data
    # print(json_post_data)
    # post_data = urllib.parse.parse_qs(json_post_data, keep_blank_values=1)
    # json_data = next(iter(post_data.keys()))
    # json_dict = json.loads(json_data)
    # return json_dict
    return json_post_data





