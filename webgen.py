import logging
import source, generator
import sys
import json

def main():
	logging.basicConfig(level=logging.DEBUG,format='%(asctime)-15s %(levelname)-5s %(name)-8s %(message)s')
	logger = logging.getLogger('webgen')
	logger.info('Generating website...')
	config = json.load(open(sys.argv[1]))
	source.copy_files(config)
	blogs = source.list_blogs(config)
	generator.generate_blogs(blogs, config)
	logger.info('Completed generating website')

if __name__ == '__main__':
	if(len(sys.argv)==1):
		sys.exit('Usage: %s path/to/config.json\nMore details at https://github.com/sakthipriyan/webgen' % sys.argv[0])
	main()