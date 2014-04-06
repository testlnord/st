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
        check = self.conn.cursor()
        for tab in check.execute("select * from sqlite_master  where type = 'table'"):
            print (tab)
        print("Database started")

    def addUser(self, name, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO user (name, email) VALUES (?, ?);", (name, email))
        self.conn.commit()

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
        cur.execute("INSERT INTO participants(user_id, tour_id, build_status, time) values (?, ?, ?, ?)",
                    (user_id, tour_id, build_status, time))
        self.conn.commit()

    def getSolutionsInTournament(self, tour_id):
        cur = self.conn.cursor()
        self.conn.commit()


def addUser(data):
    name = data["name"]
    email= data["email"]
    con = lite.connect(os.path.join(config.db_path, config.db_name))
    with con:
        cur = con.cursor()
        try:
            cur = con.cursor()
            values = wrapByComma(name)+","+wrapByComma(email)
            cur.execute("INSERT INTO user(name , email) VALUES ("+values+");")
            return 0
        except lite.IntegrityError:
            print(name+" is already there")
            return 1

def createTournament(data):
    name = data["name"]
    checker= data["checker"]
    timelimit = data["timelimit"]
    start_time = data ["start_time"]
    end_time  = data ["end_time"]

    con = lite.connect(os.path.join(config.db_path, config.db_name))
    with con:
        cur = con.cursor()
        try:
            cur = con.cursor()
            values =packArgs([wrapByComma(name),wrapByComma(checker),timelimit,start_time,end_time])
            cur.execute("INSERT INTO tournament(name , checker , timelimit , start_time, end_time) VALUES (' "+values+" ');")
            return 0
        except lite.IntegrityError:
            print(name+" is already there")
            return 1

def setUserToTournament (data):
    user_name = data["user"]
    tour_name = data["tour"]


def setSolution(self, data):
    pass

def createRun(self, data):
    pass

def createGame(self, data):
    pass


def printTable():
    con = lite.connect(os.path.join(config.db_path, config.db_name))
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id,Name FROM user;")
        print("Id \t Name")
        for row in cur:
            print(row[0],"\t",row[1])

#madnes!!!
def wrapByComma (string):
    return "'"+string+"'"

def packArgs (args):
    s=""
    for arg in args:
        s+=","+str(arg)








