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

def setUserToTournament ():
    pass

def setSolution():
    pass

def createRun():
    pass

def createGame():
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








