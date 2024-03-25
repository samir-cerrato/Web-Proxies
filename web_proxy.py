#!/usr/bin/python3
#
# Wesleyan University
# COMP 332
# Homework 3: Simple multi-threaded web proxy

# Usage:
#   python3 web_proxy.py <proxy_host> <proxy_port> <requested_url>
#

# Python modules
import socket
import sys
import threading


class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1
        self.web_cache = {}
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.bind((self.proxy_host, self.proxy_port))
            proxy_sock.listen(self.proxy_backlog)

        except OSError as e:
            print ("Unable to open proxy socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        print("Proxy server is running...")

        # Wait for client connection
        while True:
            client_conn, client_addr = proxy_sock.accept()
            print ('Client with address has connected', client_addr)
            thread = threading.Thread(
                    target = self.serve_content, args = (client_conn, client_addr))
            thread.start()

    def serve_content(self, client_conn, client_addr):

       
        try:
            # Receive length of URL data from client
            url_length_bytes = client_conn.recv(4)
            url_length = int.from_bytes(url_length_bytes, 'big')

            # Receive URL data from client based on received length
            url_data_bytes = client_conn.recv(url_length)
            url_data = url_data_bytes.decode('utf-8')

            # Extract hostname from URL
            hostname = url_data.replace("http://", "").replace("/", "")

            # Check if URL is in cache
            if hostname in self.web_cache:
                # If URL is in cache, retrieve cached response and forward to client
                cached_response = self.web_cache[hostname]
                client_conn.sendall(cached_response)
                print("Forwarding cached response to client")
            else:
                
                # Establish connection to web server
                web_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                web_server_sock.connect((hostname, 80))
                print('Connected to web server')

                # Send GET request to web server
                request = 'GET / HTTP/1.1\r\nHost: %s\r\n\r\n' % hostname
                web_server_sock.send(request.encode('utf-8'))

                # Receive data from web server
                response_data = b''
                while True:
                    data = web_server_sock.recv(4096)
                    if not data:
                        break
                    response_data += data

                # Cache the response data
                self.web_cache[hostname] = response_data

                # Send response data to client
                client_conn.sendall(response_data)
                print('Forwarding data to client')

        except Exception as e:
            print(f"Error communicating with web server: {e}")

        finally:
            # Close connection to web server
            web_server_sock.close()
            # Close connection to client
            client_conn.close()


 

def main():

    print (sys.argv, len(sys.argv))

    proxy_host = 'localhost'
    proxy_port = 50008

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    web_proxy = WebProxy(proxy_host, proxy_port)

if __name__ == '__main__':

    main()
