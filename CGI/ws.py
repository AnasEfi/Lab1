import os, sys, threading, time
from http.server import HTTPServer, CGIHTTPRequestHandler

port = 8080
webdir = '.'
if len(sys.argv) > 1:
	webdir = sys.argv[1]
if len(sys.argv) > 2:
	port = int(sys.argv[2])

def main():
	print('webdir "%s", port %s' % (webdir, port))
	os.chdir(webdir)

	serv = HTTPServer(('', port), CGIHTTPRequestHandler)
	serv.serve_forever()
	serv.send_response(200)		
	

try:
	main()
	
except:
	print("bye")

