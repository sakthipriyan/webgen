import logging
import os
import logging
import shutil
from models import BlogItem 

logger = logging.getLogger(__name__)

def list_blogs(src, gen_draft=False):
	logger.debug('Looking at src directory %s', src)
	blogs = []
	skipped = 0
	for year in os.listdir(src):
		year_dir = src + '/' + year
		for month in os.listdir(year_dir):
			month_dir = year_dir + '/' + month
			for day in os.listdir(month_dir):
				day_dir = month_dir + '/' + day
				for article in os.listdir(day_dir):
					article_path = day_dir + '/' + article
					article_path = '/'.join(article_path.split('/')[-4:])
					if gen_draft or article_path.endswith('.md') and not article_path.endswith('draft.md'):
						blogs.append(BlogItem(article_path))
					else:
						skipped = skipped + 1
	logger.debug('Total number of blogs loadded %s', len(blogs))
	logger.debug('Total number of blogs skipped %s', skipped)
	blogs.sort(key = lambda r : r.date)	
	return blogs


def copy_files(config):
	src = config['base_dir']
	web_copy = config['web_copy']
	logger.info('Source directory %s', src)
	dist = src + '/dist'
	shutil.rmtree(dist,True)
	logger.info('Website is generated at %s', dist)
	for folder in web_copy:
		shutil.copytree('%s/web/%s' % (src,folder), '%s/%s' % (dist,folder))



