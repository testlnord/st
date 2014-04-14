__author__ = 'stanis'

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from queue import Queue


import db
import threading,socket

from support import *


@support(addUser, "/add_user")
@support(addTournament,"/create_tournament")
@support(getUserInfo,"/get_user_info")
@support (add_solution,"/send_solution")
@support (add_participant,"/add_participant")
@support (run_tournament,"/run_tournament")
@support (get_run_result,"/get_run_result")
class Handler(BaseHTTPRequestHandler):
    supportedHandlers = {}

    def __init__(self,*args,**kargs):
        self.db =db.DB()
        super(BaseHTTPRequestHandler, self ).__init__(*args,**kargs)

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


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    '''
    use a thread pool instead of a new thread on every request
    '''
    numThreads = 10
    allow_reuse_address = True  # seems to fix socket.error on server restart

    def serve_forever(self):
        '''
        Handle one request at a time until doomsday.
        '''
        # set up the threadpool
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target = self.process_request_thread)
            t.setDaemon(1)
            t.start()

        # server main loop
        while True:
            self.handle_request()

        self.server_close()


    def process_request_thread(self):
        '''
        obtain request from queue instead of directly from server socket
        '''
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())


    def handle_request(self):
        '''
        simply collect requests and put them on the queue for the workers.
        '''
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            self.requests.put((request, client_address))


class Server:
    def __enter__(self):
        return self
    def run (self,host,port):
            self.serv = ThreadedHTTPServer((host,port), Handler )
            self.serv.serve_forever()
    def __exit__(self, type, value, traceback):
        if hasattr(self,'serv'):
            self.serv.socket.close()



