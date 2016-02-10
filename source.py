import os
import logging
import shutil
import datetime

logger = logging.getLogger(__name__)

def list_blogs(config):
	src = config['base_dir'] + '/src'
	gen_draft = config['gen_draft']
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
					logger.debug('Found blog in location %s', article_path)
					if gen_draft or article_path.endswith('.md') and not article_path.endswith('draft.md'):
						blogs.append(get_date_blog(article_path))
					else:
						skipped = skipped + 1
	logger.debug('Total number of blogs loadded %s', len(blogs))
	logger.debug('Total number of blogs skipped %s', skipped)
	blogs.sort(key=lambda x: x[0])
	return blogs

def copy_files(config):
	src = config['base_dir']
	web_copy = config['web_copy']
	logger.info('Source directory %s', src)
	dist = src + '/dist'
	for the_file in os.listdir(dist):
		file_path = os.path.join(dist, the_file)
		shutil.rmtree(file_path,True)
	logger.info('Website is generated at %s', dist)
	for folder in web_copy:
		shutil.copytree('%s/web/%s' % (src,folder), '%s/%s' % (dist,folder))

def get_date_blog(article_path):
	article_path_split = article_path.split('/')
	location = '/'.join(article_path_split[-4:]).replace('.md','.html')
	date_str = ''.join(article_path_split[-4:-1])
	date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
	return (date,article_path,location)
