# Web-Proxies
Working with TCP sockets and creating and parsing HTTP requests and responses.

You will implement a simple web client and
web proxy using Python. The client will request a webpage via the web proxy, and the web proxy
will return the webpage to the client.

Part 1: URLs and GET requests. You will create the web client and web proxy according to
the setup shown in Figure 1. In Figure 1, the client and web proxy both run on your local machine
using address localhost. The web server is any website on the Internet that accepts HTTP con-
nections on port 80. Your web proxy will listen on port 50008 for connections from a web client.
Note that many websites only accept HTTPS connections on port 443: you will not want to use
such websites for your testing. A few known HTTP sites to try inclulde www-db.deis.unibo.it,
httpforever.com, example.com, info.cern.ch.

• Web client. The goal of the web client is to connect to a URL, such as www.example.com
as in Figure 1. This URL should be passed to the client program via the command-line
when the client starts up. For testing, you may want to use a hard-coded default URL in
the client code. To connect to the web proxy, the client will connect to the TCP socket on
which the web proxy is listening. The client will then send an HTTP GET request into this
socket to the web proxy. For instance, suppose the client wishes to connect to:

https://info.cern.ch/hypertext/WWW/TheProject.html

Then the client GET request will have the following format, where \r\n represents the
carriage return and new line characters. The URL information contained in the host and
path in the GET request indicates the desired object to download, as well as the host to
which the web proxy will need to connect.

GET /hypertext/WWW/TheProject.html HTTP/1.1\r\n

Host: info.cern.ch\r\n\r\n

• Web proxy. The web proxy, upon receipt of this GET request, will parse out the hostname
and open a TCP connection to that host. The web proxy will then forward the GET request
to the host over this TCP connection and receive back the host’s HTTP response. The web
proxy will then forward the received response back to the client, over the TCP connection
that the web proxy has with the client

Add this line after the Host line; this will close the connection after each response from the
server, rather than requiring you to reassemble messages and determine whether you have received
a complete message. You may also find the following helpful when looking at HTTP requests and
responses.

• RFC 2616: Hypertext Transfer Protocol – HTTP/1.1. https://tools.ietf.org/html/rfc2616
