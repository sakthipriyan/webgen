import logging
import source, generator
import sys
import json
from server import start_server
from browser import start_browser, refresh_browser
from monitor import monitor

logging.basicConfig(level=logging.DEBUG,format='%(asctime)-15s %(levelname)-5s %(name)-8s %(message)s')
logger = logging.getLogger('webgen')

def generate():
	logger.info('Generating website...')
	config = json.load(open(sys.argv[1]))
	source.copy_files(config)
	blogs = source.list_blogs(config)
	generator.generate_blogs(blogs, config)
	refresh_browser()
	logger.info('Completed generating website')

def main():
	start_server('/home/crayondata.com/sakthipriyan/workspace/blog/sakthipriyan.com/dist')
	start_browser()
	monitor('/home/crayondata.com/sakthipriyan/workspace/blog/sakthipriyan.com/src', generate)

if __name__ == '__main__':
	if(len(sys.argv)==1):
		sys.exit('Usage: %s path/to/config.json\nMore details at https://github.com/sakthipriyan/webgen' % sys.argv[0])
	main()
