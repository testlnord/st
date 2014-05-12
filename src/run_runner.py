__author__ = 's'
import os
import sys
import config
import urllib.parse
import urllib.request


import util.register
import datetime
#imports
for path in config.start_list:
    if os.path.isdir(path):
        for (dir, dirs, files) in os.walk(path):
            for file in files:
                if file[-3:] == ".py":
                    exec("import %s" % (file[:-3]))
    else:
        if path[-3:] == ".py":
            exec("import %s" % (path[:-3]))


class Run_runner:
    def __init__(self):
        self.db = db.DB()


    def play_game(self, game):
        game_id = game[0]
        checker_name = game[1]
        tour_id = game[2]
        timelimit = game[3]
        s1 = dict()
        s1["user_id"], s1["runner_name"], s1["file_name"] = game[4 - 6]
        s2 = dict()
        s2["user_id"], s2["runner_name"], s2["file_name"] = game[7 - 9]

        s1["tour_id"]=tour_id
        s2["tour_id"]=tour_id

        r1 = support.make_runner(s1, timelimit)
        r2 = support.make_runner(s2, timelimit)

        checker = util.register.checkers[checker_name](r1, r2)
        checker.play()
        p1, p2 = checker.points()

        cur = self.conn.cursor()
        res = cur.execute("UPDATE game"
                          " SET points1 = ?"
                          " SET points2 = ?"
                          " SET log = ?"
                          " WHERE id = ?",
                          (p1, p2, checker.log(), game_id)
                          )
        self.conn.commit()


    def run(self):
        cur = self.db.conn.cursor()
        games = cur.execute("SELECT game.id as game_id, "
                            "tournament.checker as checker, "
                            "tournament.id as tour_id, "
                            "tournament.timelimit, "
                            #solution 1 info
                            "sol1.user_id as s1_uid, "
                            "sol1.runner_name as s1_runner_name, "
                            "sol1.out_name as s1_out_name, "
                            #solution 2 info
                            "sol2.user_id as s2_uid, "
                            "sol2.runner_name as s2_runner_name, "
                            "sol2.out_name as s2_out_name "

                            #joins
                            "FROM game"
                            "  JOIN run ON game.run = run.id"
                            "  JOIN tournament ON run.tour_id = tournament.id"
                            "  JOIN solution as sol1 ON sol1.id = game.solution1 "
                            "  JOIN solution as sol2 ON sol2.id = game.solution2"

                            #projection
                            "  WHERE game.log = ?", ('NOT PLAYED',))
        for game in games:
            self.play_game(game)

    def run_active_tours(self):
         url = 'http://'+str(config.serverHost)+':'+str(config.serverPort)+"/run_active_tours"
         response = urllib.request.urlopen(url)
         return  response

def add_cron_entry():
    shabang = "#!/bin/bash"
    PATH = "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    CUR_PATH=os.path.dirname(__file__)

    script = os.path.abspath(__file__)
    python = sys.executable
    logging = " >> /tmp/surreal_tournament.log"

    command ="cd %s && "%CUR_PATH + python +" run_runner.py"+logging

    cur_cron = os.popen('crontab -l > current_crontab.txt')
    cur_cron.read()
    cur_cron.close()

    if command not in open('current_crontab.txt').read():
        fp = open('current_crontab.txt',"r+")
        if len(fp.readlines()) is 0:
             print("%s " %shabang,file=fp)
             print("%s " %PATH,file=fp)

        print("* * * * * %s " %command,file=fp)
        fp.close()
        load = os.popen('crontab current_crontab.txt')
        load.read()
        load.close()
    os.remove("current_crontab.txt")



if __name__ == "main":
    now = datetime.datetime.now()
    print("run runner has been run at  %s" %now)
    runner = Run_runner()
    runner.run_active_tours()

