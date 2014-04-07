#from unittest.test import support
import datetime
import os


__author__ = 'stanis'

import http.server
import socketserver
import urllib.parse

import json
import db


from support import *


@supprort(addUser, "/add_user")
@supprort(addTournament,"/create_tournament")
@supprort(getUserInfo,"/get_user_info")


class Handler(http.server.BaseHTTPRequestHandler):
    supportedHandlers = {}

    def __init__(self):
        self.db =db.DB()
        super(http.server.BaseHTTPRequestHandler, self ).__init__()

    def getKeyFromAddres(self,str):
        return str.split('?')[0]

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        key = self.getKeyFromAddres(self.path)
        self.wfile.write(self.supportedHandlers[key](self.db,self.path))
        self.wfile.close()

    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()

        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'),keep_blank_values=1)


        jsonData=next(iter(post_data.keys()))
        jsonData = json.loads(jsonData)

        key = self.getKeyFromAddres(self.path)
        self.supportedHandlers[key](self.db,jsonData,self.path)


class Server:
    def __enter__(self):
        return self
    def run (self,host,port):
            self.serv = socketserver.TCPServer((host,port), Handler )
            self.serv.serve_forever()
    def __exit__(self, type, value, traceback):
        if hasattr(self,'serv'):
            self.serv.socket.close()



