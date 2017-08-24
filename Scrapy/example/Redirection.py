"""
URL redirection example.
"""

import BaseHTTPServer
import time
import sys


HOST_NAME = '127.0.0.1' # HOSE_NAME must be 127.0.0.1
PORT_NUMBER = 9000 # Maybe set this to 9000.
REDIRECTIONS = {"/slashdot/": "http://slashdot.org/",
                "/freshmeat/": "http://freshmeat.net/"}
LAST_RESORT = "http://www.baidu.com"

class RedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def doHEAD(s):
        s.send_response(301)
        s.send_header("Location", REDIRECTIONS.get(s.path, LAST_RESORT))
        s.end_headers()
    def do_GET(s):
        s.doHEAD()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), RedirectHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)