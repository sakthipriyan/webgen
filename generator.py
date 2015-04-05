from jinja2 import Environment, FileSystemLoader
from models import Blog, Link, Item, List
import logging
import collections
import markdown
import os

logger = logging.getLogger(__name__)

def generate_blogs(files, config):
	generated_blogs = []
	for f in files:
		logger.debug('Processing file %s' % f[1])
		with open (f[1], "r") as md_file:
			content = md_file.readlines()
			if(len(content) < 4):
				logger.warn('File %s Contains less than 4 lines, skipping' % f[1])
				continue
			blog = get_blog(config, content, f)
			generated_blogs.append(blog)
	link_prev_next(generated_blogs)
	publish_home(config, generated_blogs)
	publish_blogs(config, generated_blogs)
	publish_tags(config, generated_blogs)
	#publishCalendar(config, data)

def get_blog(config, content, f):
	title = content[0].strip()
	sub_title = content[1].strip()
	tags =  get_tags(config, content[2])
	md = ''.join(content[3:])
	html = markdown.markdown(md)
	link = Link(title, config['base_uri'] + config['blogs_dir'] + f[2])
	return Blog(path=f[2], title=title, sub_title=sub_title, 
		date=f[0], html=html, tags=tags, current=link)

def get_tags(config, line3):
	tags = [s.strip() for s in line3.split(',')]
	tags_link = []
	for tag in tags:
		link = Link(tag,  config['base_uri'] + config['tags_dir'] + tag.lower().replace(' ', '_') + '.html')
		tags_link.append(link)
	return tags_link

def link_prev_next(generated_blogs):
	prev_blog = None
	next_blog = None
	for index, current_blog in enumerate(generated_blogs):
		if(len(generated_blogs) > index + 1):
			next_blog = generated_blogs[index+1]
		else:
			next_blog = None
		if prev_blog is not None:
			current_blog.prev = prev_blog.current
		if next_blog is not None:
			current_blog.next = next_blog.current
		prev_blog = current_blog

def publish_home(config, generated_blogs):
	logger.info('Generating home page')
	blog = generated_blogs[-1]
	blogs = reversed(generated_blogs[1:config['home_recent_count']+1])
	template = get_template(config, 'home.html')
	html = template.render(
		base_uri=config['base_uri'],
		js=config['html']['js'],
		css=config['html']['css'],
		blog=blog,
		blogs=blogs)
	write_file(config['base_dir'] + '/dist/' + 'index.html', html)

def publish_blogs(config, generated_blogs):
	logger.info('Generating blog pages')
	data = {}
	for blog in generated_blogs:
		template = get_template(config, 'blog.html')
		html = template.render(
			base_uri=config['base_uri'],
			js=config['html']['js'],
			css=config['html']['css'],
			title=blog.title,
			data=blog)
		filename = config['base_dir'] + '/dist/' + config['blogs_dir'] + blog.path
		write_file(filename, html)
	return data

def publish_tags(config, generated_blogs):
	data = {}
	for blog in generated_blogs:
		item = Item(blog.current.href, blog.date, blog.title, blog.sub_title, blog.tags)
		for tag in blog.tags:
			a = tag.href
			tag_key =  a[a.rindex('/')+1:a.rindex('.')]
			add_key_value(data, tag_key, item)
	data = collections.OrderedDict(sorted(data.items()))
	logger.info('Generating tags pages')
	template = get_template(config, 'list.html')
	for key in data:
		list_page = List('Tags / ' + key.replace('_',' '),data[key],None,None)
		html = template.render(
			base_uri=config['base_uri'],
			js=config['html']['js'],
			css=config['html']['css'],
			title=list_page.title,
			list=list_page
			)
		filename = config['base_dir'] + '/dist/' + config['tags_dir'] + key + '.html'
		write_file(filename, html)

def get_template(config, template_file):
	base_dir = config['base_dir']
	env = Environment(loader=FileSystemLoader(base_dir + '/web/html'))
	return env.get_template(template_file)

def write_file(filename, content):
	logger.debug('Writing content to file ' + filename)
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename, "w") as f:
		f.write(content)
		f.close()

def publishCalendar(config, data):
	pass

def publishTags(config, data):
	pass

def generateCalendar(blogs,config):
	logger.debug('Generating calendar')
	count = 0
	calendar = {}
	for blog in blogs:
		y = str(blog.date.year)
		ym = y + two_digit(blog.date.month)
		ymd = ym + two_digit(blog.date.day)
		add_to_dict_array(calendar, y, blog)
		add_to_dict_array(calendar, ym, blog)
		add_to_dict_array(calendar, ymd, blog)

	od = collections.OrderedDict(sorted(calendar.items()))
	logger.debug('%s pages generated for calendar' % count)

def two_digit(number):
	if number > 9:
		return str(number)
	else:
		return '0' + str(number)

def add_to_dict_array(dictArray,key,value):
	if dictArray.has_key(key):
		dictArray[key] = [value] + dictArray[key]
	else:
		dictArray[key]=[value]

def add_key_value(data,key,value):
	if data.has_key(key):
		data[key] = [value] + data[key]
	else:
		data[key]=[value]
