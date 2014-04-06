__author__ = 'stanis'

import http.server
import socketserver
import urllib.parse

import json
import db


def supprort(method,key):
    def adder(handler):
        handler.supportedHandlers[key]=method
        return handler
    return adder


@supprort(db.addUser, "/add_user")
@supprort(db.createTournament,"/create_tournament")
class Handler(http.server.BaseHTTPRequestHandler):
    supportedHandlers = {}

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        s="<html><head><title>That is surreal tournament.</title></head>"
        self.wfile.write(s.encode("utf-8"))
        s="<body><p>U can create user by sending POST with json to /add_user </p>"
        self.wfile.write(s.encode("utf-8"))
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s="<p>You accessed path: %s</p>" % self.path
        self.wfile.write(s.encode("utf-8"))
        self.wfile.write(bytes(("</body></html>"), "utf-8"))
        self.wfile.close()





    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()

        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'),keep_blank_values=1)


        jsonData=next(iter(post_data.keys()))
        jsonData = json.loads(jsonData)

        key = self.path
        self.supportedHandlers[key](jsonData)


class Server:
    def __enter__(self):
        return self
    def run (self,host,port):
            self.serv = socketserver.TCPServer((host,port), Handler )
            self.serv.serve_forever()
    def __exit__(self, type, value, traceback):
        if hasattr(self,'serv'):
            self.serv.socket.close()



