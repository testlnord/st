__author__ = 'stanis'

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from queue import Queue

import traceback

import db
import threading, socket

from config import num_of_server_threads

from support import *

class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kargs):
        self.db = db.DB()
        super(BaseHTTPRequestHandler, self).__init__(*args, **kargs)

    @staticmethod
    def get_key_from_addres(str):
        return str.split('?')[0]

    def do_GET(self):


        key = self.get_key_from_addres(self.path)
        try:
            data = supportedHandlers[key](self.db, self.path)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if data is not None:
                self.wfile.write(data)

        except Exception as e:
             print(e)

             print (e.with_traceback(e.__traceback__))
             self.send_response(400)
             self.send_header('content-type', "application/json")
             self.end_headers()
             tb = traceback.format_exc().encode("utf-8")
             self.wfile.write(tb)
        #except:
        #    self.send_response(400)
        #    self.send_header("Content-type", "application/json")
        #    self.end_headers()

        #self.wfile.close()

    def do_POST(self):


        length = int(self.headers.get('content-length'))

        try:
            data = self.rfile.read(length).decode('utf-8')
            key = self.get_key_from_addres(self.path)
            data = supportedHandlers[key](self.db, data, self.path)
            self.send_response(200)
            self.send_header('content-type', "application/json")
            self.end_headers()
            if data is not None:
                print(data)
                self.wfile.write(data)


        except Exception as e:
             print(e)

             print (e.with_traceback(e.__traceback__))
             self.send_response(400)
             self.send_header('content-type', "application/json")
             self.end_headers()
             tb = traceback.format_exc().encode("utf-8")
             self.wfile.write(tb)

        self.wfile.write.close()



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    use a thread pool instead of a new thread on every request
    """
    numThreads = num_of_server_threads
    allow_reuse_address = True  # seems to fix socket.error on server restart

    def serve_forever(self):
        """
        Handle one request at a time until doomsday.
        """
        # set up the threadpool
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target=self.process_request_thread)
            t.setDaemon(1)
            t.start()

        # server main loop
        while True:
            self.handle_request()

        self.server_close()

    def process_request_thread(self):
        """
        obtain request from queue instead of directly from server socket
        """
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())

    def handle_request(self):
        """
        simply collect requests and put them on the queue for the workers.
        """
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            self.requests.put((request, client_address))


class Server:
    def __enter__(self):
        return self

    def run(self, host, port):
        self.serv = ThreadedHTTPServer((host, port), Handler)
        self.serv.serve_forever()

    def __exit__(self, type, value, traceback):
        if hasattr(self, 'serv'):
            self.serv.socket.close()



