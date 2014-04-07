#from unittest.test import support

import os
import socket


__author__ = 'stanis'

import http.server
import socketserver
import urllib.parse

import json
import db


from support import *


@support(addUser, "/add_user")
@support(addTournament,"/create_tournament")
@support(getUserInfo,"/get_user_info")
@support (add_solution,"/send_solution")
@support (add_participant,"/add_participant")
@support (run_tournament,"/run_tournament")
@support (get_run_result,"/get_run_result")
class Handler(http.server.BaseHTTPRequestHandler):
    supportedHandlers = {}

    def __init__(self,*args,**kargs):
        self.db =db.DB()
        super(http.server.BaseHTTPRequestHandler, self ).__init__(*args,**kargs)

    def getKeyFromAddres(self,str):
        return str.split('?')[0]

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        key = self.getKeyFromAddres(self.path)
        data=self.supportedHandlers[key](self.db,self.path)
        if data != None:
            self.wfile.write(data)


    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()

        key = self.getKeyFromAddres(self.path)
        # print(self.rfile.read().decode('utf-8'))
        self.supportedHandlers[key](self.db,self.rfile,self.path)





class Server:
    def __enter__(self):
        return self
    def run (self,host,port):
            self.serv = socketserver.TCPServer((host,port), Handler )
            self.serv.serve_forever()
    def __exit__(self, type, value, traceback):
        if hasattr(self,'serv'):
            self.serv.socket.close()



