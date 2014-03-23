__author__ = 'stanis'

import http.server
import socketserver


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        # self.wfile.write("hello I'm doing get!")

        print(self.command)
        print(self.request)
        print(self.path)
        print()

        print("I'm doing GET")
    def do_POST(self):
        print("I'm doing POST")


try:
    serv = socketserver.TCPServer(("localhost",8080), Handler )
    serv.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    serv.socket.close()