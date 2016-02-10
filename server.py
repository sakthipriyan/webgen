from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import threading, time, os, logging

logging.basicConfig(level=logging.DEBUG,format='[%(asctime)-15s] %(levelname)-5s %(name)-8s %(message)s')
server_logger = logging.getLogger(__name__)
hostname = 'localhost'
port = 8000

class CustomSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        server_logger.debug(format%args)

def start_server(directory):
    os.chdir(directory)
    server = HTTPServer(('localhost', 8000), CustomSimpleHTTPRequestHandler)
    thread = threading.Thread(target = server.serve_forever)
    thread.daemon = True
    thread.start()
    server_logger.info('Launched web server in %s:%d' % (hostname, port))
