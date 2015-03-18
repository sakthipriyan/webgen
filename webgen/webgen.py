import logging
import source
import sys
import shutil
import json


if(len(sys.argv)==1):
	sys.exit('Usage: %s /path/to/config.json\nMore details at https://github.com/sakthipriyan/webgen' % sys.argv[0])

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
logger = logging.getLogger(__name__)
logger.info('Generating website...')
config = json.load(open(sys.argv[1]))
src = config['base_dir']
dist = src + '/dist'
logger.info('Source directory %s', src)
shutil.rmtree(dist,True)
logger.info('Website is generated at %s', dist)
for folder in config['web_copy']:
	shutil.copytree('%s/web/%s' % (src,folder), '%s/%s' % (dist,folder))

print(source.listBlogs(src + '/src'))
