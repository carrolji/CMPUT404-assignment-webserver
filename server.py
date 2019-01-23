#  coding: utf-8 
import socketserver
import os

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

        # Convert byte to string
        string = self.data.decode("utf-8")
        
        # Get method and path from request-url line
        req_line = string.split('HTTP')[0].split(' ')
        method = req_line[0]
        path = req_line[1]
        
        file_name = ''
        cont_type = ''

        if method == 'GET':
            file_name = './www' + path

            code = '200 OK\r\n'
            cont_type = 'Content-Type: text/html\r\n'

            if 'css' in path:
                cont_type = 'Content-Type: text/css\r\n'
            
            elif os.path.exists(file_name) and 'html' not in path:
                file_name += 'index.html'


        try:
            with open(file_name, 'r') as html_file:
                content = html_file.read()

        except OSError as e:
            if method != 'GET':
                #405 Method Not Allowed, POST/PUT/DELETE
                code = '405 Method Not Allowed\r\n'
            else:
                code = '404 Not Found\r\n'
            
            content = '<head><title>%s</title></head><h1>%s</h1>' % (code ,code)
            

        response = 'HTTP/1.1 '+ code + cont_type + '\r\n' + content + '\r\n'
        self.request.sendall(bytearray(response, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
