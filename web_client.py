#!/usr/bin/python3
#
# Wesleyan University
# COMP 332
# Homework 3: Simple web client to interact with proxy
#
# Example usage:
#
#   python3 web_client.py <proxy_host> <proxy_port> <requested_url>

# Python modules
import binascii
import socket
import sys

class WebClient:

    def __init__(self, proxy_host, proxy_port, url):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.url = url
        self.start()

    def start(self):

        # Open connection to proxy
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.connect((self.proxy_host, self.proxy_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        
        requested_url = self.url.encode('utf-8')
        proxy_sock.send(len(requested_url).to_bytes(4, 'big'))
        proxy_sock.send(requested_url)


        # Receive binary data from proxy
        response_data = b""
        while True:
            data = proxy_sock.recv(4096)
            if not data:
                break
            response_data += data

        print("Response from web proxy:")
        print(response_data.decode('utf-8'))

        

        proxy_sock.close()

def main():

    print (sys.argv, len(sys.argv))
    proxy_host = 'localhost'
    proxy_port = 50008
    url = 'http://example.com/'
    #url = 'http://eu.httpbin.org'
    #url = 'http://info.cern.ch/'
    #url = 'http://www-db.deis.unibo.it/'
    #url = 'http://info.cern.ch/hypertext/WWW/TheProject.html'

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])
        url = sys.argv[3]

    web_client = WebClient(proxy_host, proxy_port, url)

if __name__ == '__main__':
    main()
