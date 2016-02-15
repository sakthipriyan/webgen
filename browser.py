import os, subprocess
import threading, time
import requests, json
import logging
from websocket import create_connection
from server import hostname, port

chrome_port = 9222
refresh_json = json.dumps({
    "id": 0,
    "method": "Page.reload",
    "params": {
       "ignoreCache": True,
       "scriptToEvaluateOnLoad": ""
     }
 })
hostname_port = '%s:%d' %(hostname,port)
logger = logging.getLogger(__name__)

def open_browser(url):
    directory = os.path.join(os.path.expanduser('~'), '.webgen-profile')
    command = 'google-chrome --remote-debugging-port=%d --user-data-dir=%s %s' % (chrome_port,directory,url)
    subprocess.call(command, shell=True)

def refresh_browser():
    response = requests.get('http://%s:%s/json' %(hostname,chrome_port))
    for page in response.json():
        if  page['type'] == 'page' and hostname_port in page['url']:
                logger.info('Refreshing page %s' % page['url'])
                ws = create_connection(page['webSocketDebuggerUrl'])
                ws.send(refresh_json)
                ws.close()

def start_browser():
    thread = threading.Thread(target = open_browser, kwargs={'url':'http://localhost:8000'})
    thread.daemon=True
    thread.start()
