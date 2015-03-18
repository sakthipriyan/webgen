import logging
import source
import sys
import json

def main():
	logging.basicConfig(level=logging.DEBUG,format='%(asctime)-15s %(levelname)s %(name)s %(message)s')
	logger = logging.getLogger(__name__)
	logger.info('Generating website...')
	config = json.load(open(sys.argv[1]))
	source.copy_files(config)
	src = config['base_dir']
	source.list_blogs(src + '/src')
	logger.info('Completed')

if __name__ == '__main__':
	if(len(sys.argv)==1):
		sys.exit('Usage: %s /path/to/config.json\nMore details at https://github.com/sakthipriyan/webgen' % sys.argv[0])
	main()
