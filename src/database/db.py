import os
import config
import json

__author__ = 's'
import sqlite3 as lite
import datetime
import sys


class DB:
    tables = ["user", "tournament", ""]

    def __init__(self):
        self.conn = lite.connect(os.path.join(config.db_path, config.db_name))
        print("Database started")

    def self_test(self):
        print("self_test")
        print("add_uiser")
        self.addUser("asdf", "asdf")
        print("get_user")
        print(self.getUser(name="asdf"))
        print("add tour")
        self.addTournament("asdf", "gasdf", 2, "24.01.1099", "gjfvj2014")
        print("get tour")
        print(self.getTournament(name="asdf"))
        print("add part")
        self.addParticipant(1, 1)
        print("get part")
        print(self.getParticipantsInTournament(1))
        print("add sol")
        self.addSolution(1, 1, 0, "21321", "cpp", "a.out")
        print("get sol")
        self.getSolutionsInTournament(1)

    def addUser(self, name, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO user (name, email) VALUES (?, ?);", (name, email))
        self.conn.commit()
        return cur.lastrowid

    def getUser(self, id=None, name=None):
        cur = self.conn.cursor()
        query = "SELECT name, email, id FROM user "
        if (not id is None):
            res = cur.execute(query + "where id = ?", (id,))
        elif (not name is None):
            res = cur.execute(query + "where name = ?", (name,))
        else:
            res = cur.execute(query)
        result = []
        for (user_name, user_mail, user_id) in res:
            result.append({"name": user_name, "email": user_mail, "id": user_id})

        return result

    def checkUserInTour (self,name,t_name):
        cur = self.conn.cursor()
        cur.execute("SELECT user.name , tournament.name "
                    "FROM user JOIN participants ON (user.id = participants.user_id) JOIN tournament ON (participants.tour_id = tournament.id)"
                    "WHERE user.name = ? AND tournament.name = ?", (name,t_name))
        if len(cur.fetchall())>0:
            return [True]
        else:
            return [False]


    def addTournament(self, name, checker, timelimit, start_time, end_time):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tournament(name, checker, timelimit, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
                    (name, checker, timelimit, start_time, end_time))
        self.conn.commit()
        return cur.lastrowid


    def getTournament(self, id=None, name=None):
        cur = self.conn.cursor()
        query = "SELECT name, checker, timelimit, start_time, end_time, id FROM tournament "
        if (not id is None):
            res = cur.execute(query + "where id = ?", (id,))
        elif (not name is None):
            res = cur.execute(query + "where name = ?", (name,))
        else:
            res = cur.execute(query)
        result = []
        for (t_name, t_checker, t_timelimit, t_s_time, t_e_time, t_id) in res:
            result.append({"name": t_name,
                           "c": t_checker,
                           "tl": t_timelimit,
                           "start_time": t_s_time,
                           "end_time": t_e_time,
                           "id": t_id})
        return result

    def addParticipant(self, tour_id, user_id):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO participants(user_id, tour_id) VALUES (?, ?)", (user_id, tour_id))
        self.conn.commit()
        return cur.lastrowid

    def addParticipantByNames(self, tour_name, user_name):
        user = self.getUser(name=user_name)
        tour = self.getTournament(name=tour_name)
        return self.addParticipant(tour[0]["id"], user[0]["id"])


    def getParticipantsInTournament(self, tour_id):
        cur = self.conn.cursor()
        res = cur.execute("SELECT name, email, id FROM user INNER JOIN participants ON user_id = id WHERE tour_id = ?",
                          (tour_id,))
        result = []
        for (user_name, user_mail, user_id) in res:
            result.append({"name": user_name, "email": user_mail, "id": user_id})

        return result

    def addSolution(self, user_id, tour_id, build_status, time, runner, file_name):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO solution(user_id, tour_id, build_status, time, runner_name, out_name) " +
                    "values (?, ?, ?, ?, ?, ?)",
                    (user_id, tour_id, build_status, time, runner, file_name))
        self.conn.commit()
        return cur.lastrowid

    def getSolutionsInTournament(self, tour_id):
        cur = self.conn.cursor()
        res = cur.execute("SELECT user_id, tour_id, build_status, max(time), id, runner_name, out_name from solution " +
                          "where tour_id = ? and build_status = 0 " +
                          "group by tour_id, user_id, id, build_status, runner_name, out_name",
                          (tour_id,))
        result = []
        for (user_id, t_id, b_status, time, id, runner, file_name) in res:
            result.append({"user_id": user_id,
                           "tour_id": t_id,
                           "build_status": b_status,
                           "time": time,
                           "id": id,
                           "runner_name": runner,
                           "file_name": file_name})
        return result

    def addRun(self, tour_id,timestart):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO run(tour_id,timestart) VALUES (?, ?)",
                    (tour_id, timestart))
        self.conn.commit()
        return cur.lastrowid

    def addGame(self, run_id, sol_id1, sol_id2, pts1, pts2, log):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO game(solution1, solution2, points1, points2, run, log) VALUES(?, ?, ?, ?, ?, ?)",
                    (sol_id1, sol_id2, pts1, pts2, run_id, log))
        self.conn.commit()
        return cur.lastrowid

    def getRunResult(self,tour_name):
        cur = self.conn.cursor()
        print (tour_name)
        run_id = cur.execute("SELECT run.id FROM run"
                             " JOIN tournament ON run.tour_id = tournament.id"
                             " WHERE tournament.name = ?"
                             " ORDER BY run.timestart DESC", (tour_name, ))
        run_id= list(run_id)
        if not run_id:
            return []
        run_id = run_id[0][0]
        res = cur.execute("SELECT sol_id, sum(pts) from (" +
                          "SELECT solution1 as sol_id, points1 as pts from game where run = ? " +
                          "UNION " +
                          "SELECT solution2 as sol_id, points2 as pts from game where run = ?" +
                          ") group by sol_id", (run_id, run_id))
        res = list(res)
        result = []
        for (sol_id,pts) in res:
            result.append({"solution": sol_id, "points": pts})

        return result


    def getFreshTourResults(self, tour_name):
        tour_info = self.getTournament(name=tour_name)
        if not tour_info:
            return []
        tour_info = tour_info[0]

        cur = self.conn.cursor()
        res = cur.execute("SELECT timestart, id from run where tour_id = ? order by timestart", tour_info["id"])

        if not res:
            return []
        return self.getRunResult(res[0][1])

    def get_active_tours (self):
        cur = self.conn.cursor()
        now = datetime.datetime.now()
        res = cur.execute("SELECT id , timelimit, checker"
                    " FROM tournament"
                    " WHERE tournament.start_time < ? AND tournament.end_time > ? ", (now,now))
        result = []
        for (id , tl , c) in res:
            result.append({'id' : id , 'tl' : tl, 'c' : c})

        return result


