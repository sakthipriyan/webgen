import pyinotify, time
import asyncore
import logging

logging.basicConfig(level=logging.DEBUG,format='[%(asctime)-15s] %(levelname)-5s %(name)-8s %(message)s')
logger = logging.getLogger(__name__)

mask =  pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, fn, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.function = fn

    def process_IN_DELETE(self, event):
        logger.debug('File deleted:' + event.path)
        self.function()

    def process_IN_CLOSE_WRITE(self, event):
        logger.debug('File edited:' + event.path)
        self.function()

def hello():
    print('hello')

def monitor(directory, callback):
    wm = pyinotify.WatchManager()
    notifier = pyinotify.AsyncNotifier(wm,EventHandler(callback))
    wm.add_watch(directory,mask,rec=True,auto_add=True)
    asyncore.loop()
