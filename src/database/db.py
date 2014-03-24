from config import db_path

__author__ = 's'
import sqlite3 as lite
import sys

def addUser(name):
    con = lite.connect('/st.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Users(Id INTEGER PRIMARY KEY, Name TEXT UNIQUE );")
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO Users(Name) VALUES ('"+name+"');")
            return 0
        except lite.IntegrityError:
            print(name+" is already there")
            return 1
def printTable():
    con = lite.connect('st.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id,Name FROM Users;")
        print("Id \t Name")
        for row in cur:
            print(row[0],"\t",row[1])

addUser('Vasya')








