import json
import zmq
import sys
import threading
import time
from random import randint, random
import db
import ast

from config import num_of_server_threads
from config import serverPort
from support import *

__author__ = "s"


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = 'worker-%d' % self.id
        socket.identity = identity.encode('utf-8')
        socket.connect('tcp://127.0.0.1:%s',serverPort)
        print('Client %s started' % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            print('Req #%d sent..' % (reqs))
            socket.send_string('request #%d' % (reqs))
            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    msg = socket.recv()
                    tprint('Client %s received: %s' % (identity, msg))
        socket.close()
        context.term()

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:%s'%serverPort)


        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(num_of_server_threads):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        poll = zmq.Poller()
        poll.register(frontend, zmq.POLLIN)
        poll.register(backend,  zmq.POLLIN)

        while True:
            sockets = dict(poll.poll())
            if frontend in sockets:
                ident, msg = frontend.recv_multipart()
                tprint('Server received %s id %s' % (msg, ident))
                backend.send_multipart([ident, msg])
            if backend in sockets:
                ident, msg = backend.recv_multipart()
                tprint('Sending to frontend %s id %s' % (msg, ident))
                frontend.send_multipart([ident, msg])

        frontend.close()
        backend.close()
        context.term()

class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context

    def jsonify(self,data):
        jsonData = json.dumps(data)
        return jsonData.encode("utf-8")

    def run(self):
        self.db = db.DB()
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        while True:
            ident, msg = worker.recv_multipart()
            tprint('Worker received %s from %s' % (msg, ident))
            json_dict = json.loads(msg.decode("utf-8"))
            json_dict=ast.literal_eval(json_dict)
            data = supportedHandlers[json_dict["key"]](self.db, json_dict)
            if data is None:
                data = self.jsonify({"ok":"ok"})
            worker.send_multipart([ident, data])
        worker.close()

def main():
    """main function"""
    server = ServerTask()
    server.start()
    for i in range(3):
        client = ClientTask(i)
        client.start()

    server.join()

if __name__ == "__main__":
    main()