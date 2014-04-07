import os
import config
import json

__author__ = 's'
import sqlite3 as lite
import sys


class DB:
    tables = ["user", "tournament", ""]
    def __init__(self):
        self.conn = lite.connect(os.path.join(config.db_path, config.db_name))
        print("Database started")


    def self_test(self):
        print("self_test")
        print("add_uiser")
        self.addUser("asdf","asdf")
        print("get_user")
        print(self.getUser(name="asdf"))
        print("add tour")
        self.addTournament("asdf","gasdf",2, "24.01.1099", "gjfvj2014")
        print("get tour")
        print(self.getTournament(name = "asdf"))
        print("add part")
        self.addParticipant(1,1)
        print("get part")
        print(self.getParticipantsInTournament(1))
        print("add sol")
        self.addSolution(1,1,0,"21321")
        print("get sol")
        self.getSolutionsInTournament(1)

    def addUser(self, name, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO user (name, email) VALUES (?, ?);", (name, email))
        self.conn.commit()
        return cur.lastrowid

    def getUser(self, id = None, name = None):
        cur = self.conn.cursor()
        query  = "SELECT name, email, id FROM user "
        if (not id is None):
            res = cur.execute(query + "where id = ?", (id,))
        elif (not name is None):
            res = cur.execute(query + "where name = ?", (name,))
        else:
            res = cur.execute(query)
        result = []
        for (user_name, user_mail, user_id) in res:
            result.append({"name":user_name, "email": user_mail, "id": user_id})

        return result

    def addTournament(self, name, checker, timelimit, start_time, end_time):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tournament(name, checker, timelimit, start_time, end_time) values (?, ?, ?, ?, ?)",
            (name, checker, timelimit, start_time, end_time))
        self.conn.commit()
        return cur.lastrowid

    def getTournament(self, id = None, name = None):
        cur = self.conn.cursor()
        query  = "SELECT name, checker, timelimit, start_time, end_time, id FROM tournament "
        if (not id is None):
            res = cur.execute(query + "where id = ?", (id,))
        elif (not name is None):
            res = cur.execute(query + "where name = ?", (name,))
        else:
            res = cur.execute(query)
        result = []
        for (t_name, t_checker, t_timelimit, t_s_time, t_e_time, t_id) in res:
            result.append({"name": t_name,
                           "checker": t_checker,
                           "timelimit": t_timelimit,
                           "start_time": t_s_time,
                           "end_time": t_e_time,
                           "id" : t_id})
        return result

    def addParticipant(self, tour_id, user_id):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO participants(user_id, tour_id) values (?, ?)", (user_id, tour_id))
        self.conn.commit()
        return cur.lastrowid
    def addParticipantByNames(self, tour_name, user_name):
        user = self.getUser(name= user_name)
        tour = self.getTournament(name= tour_name)
        return self.addParticipant(tour[0]["id"], user[0]["id"])


    def getParticipantsInTournament(self, tour_id):
        cur = self.conn.cursor()
        res = cur.execute("SELECT name, email, id from user INNER JOIN participants on user_id = id where tour_id = ?",
                    (tour_id,))
        result = []
        for (user_name, user_mail, user_id) in res:
            result.append({"name":user_name, "email": user_mail, "id": user_id})

        return result

    def addSolution(self, user_id, tour_id, build_status, time):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO solution(user_id, tour_id, build_status, time) values (?, ?, ?, ?)",
                    (user_id, tour_id, build_status, time))
        self.conn.commit()
        return cur.lastrowid

    def getSolutionsInTournament(self, tour_id):
        cur = self.conn.cursor()
        res = cur.execute("SELECT user_id, tour_id, build_status, max(time), id from solution "+
                          "where tour_id = ? group by tour_id, user_id, id, build_status", (tour_id,))
        result = []
        for (user_id, t_id, b_status, time, id) in res:
            result.append({"user_id":user_id,
                           "tour_id": t_id,
                           "build_status": b_status,
                           "time": time,
                           "id": id})
        return result

    def addRun(self, tour_id, timestart):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO run(tour_id, timestart) values (?, ?)",
                    (tour_id, timestart))
        self.conn.commit()
        return cur.lastrowid

    def addGame(self, run_id, sol_id1, sol_id2, pts1, pts2, log):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO game(solution1, solution2, points1, points2, run, log) values(?, ?, ?, ?, ?, ?)",
            (sol_id1, sol_id2, pts1, pts2, run_id, log))
        self.conn.commit()
        return cur.lastrowid


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



