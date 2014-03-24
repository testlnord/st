__author__ = 'stanis'

import http.server
import socketserver
import urllib.parse
import database.db as db

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        # self.wfile.write("hello I'm doing get!")



    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()

        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        db.addUser(post_data['User'][0])
        # print(post_data['User'][0])
        # for key, value in post_data.items():
        #     print ("%s=%s" % (key, value))


class Server:
    def __enter__(self):
        return self
    def run (self,host,port):
        try:
            self.serv = socketserver.TCPServer(("localhost",8080), Handler )
            self.serv.serve_forever()
        except KeyboardInterrupt:
            print('^C received, shutting down server')
            self.serv.socket.close()
    def __exit__(self, type, value, traceback):
        if hasattr(self,'serv'):
            self.serv.socket.close()

with  Server() as s:
    s.run("localhost",8080)

