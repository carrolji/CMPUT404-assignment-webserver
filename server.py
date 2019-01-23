#  coding: utf-8 
import socketserver
from pathlib import Path  # for checking if files exist

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Peter Weckend
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(self.data)
        #print ("Got a request of: %s\n" % self.data)
        string = self.data.decode("utf-8")
        receive = string.split('\r\n')[0]
        
        # file_name = './www/error.html'
        # code = '404 Not Found\r\n'
        # cont_type = 'Content-Type: text/html\r\n'
        file_name = ''
        code = ''
        cont_type = ''

        if 'GET' not in receive:
            #405 Method Not Allowed
            file_name = './www/error.html'
            code = '405 Method Not Allowed\r\n'
        elif ('deep/' in receive) or ('deep/index.html' in receive):
            file_name = './www/deep/index.html'
        elif (receive == 'GET / HTTP/1.1') or ('index.html' in receive):
            #file_name = './www/index.html'
            file_name = './www/index.html'
            code = '200 OK\r\n'
        elif ('base.css' in receive):
            file_name = './www/base.css'
            cont_type = 'Content-Type: text/css\r\n'
            code = '200 OK\r\n'
        elif 'deep.css' in receive:
            file_name = './www/deep/deep.css'
            cont_type = 'Content-Type: text/css\r\n'
            code = '200 OK\r\n'

        try:
            with open(file_name, 'r') as html_file:
                content = html_file.read()
        except OSError as e:
            file_name = './www/error.html'
            code = '404 Not Found\r\n'
            with open(file_name, 'r') as html_file:
                content = html_file.read()

        
        #response = 'HTTP/1.1 %s %s \r\n %s \r\n' % (code, cont_type, content)
        response = 'HTTP/1.1 '+ code + cont_type + '\r\n' + content + '\r\n'
        print("YARRRRRR       ", response)
        self.request.sendall(bytearray(response, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
