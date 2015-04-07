from jinja2 import Environment, FileSystemLoader
from models import Blog, Link, Item, List, Tag
import logging
import collections
import markdown
import os, shutil

logger = logging.getLogger(__name__)
months = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

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
	publish_calendar(config, generated_blogs)

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
	start = len(generated_blogs) - config['home_recent_count'] - 1
	blogs = reversed(generated_blogs[start:-1])
	template = get_template(config, 'home.html')
	html = template.render(
		base_uri=config['base_uri'],
		js=config['html']['js'],
		css=config['html']['css'],
		blog=blog,
		blogs=blogs,
		title='Home')
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
	logger.info('Generating tags pages')
	data = {}
	for blog in generated_blogs:
		item = Item(blog.current.href, blog.date, blog.title, blog.sub_title, blog.tags)
		for tag in blog.tags:
			a = tag.href
			tag_key =  a[a.rindex('/')+1:a.rindex('.')]
			add_key_value(data, tag_key, item)
	data = collections.OrderedDict(sorted(data.items()))
	template = get_template(config, 'list.html')
	tag_list = generate_tags_list(config,data)

	for tag_page in tag_list:
		html = template.render(
			base_uri=config['base_uri'],
			js=config['html']['js'],
			css=config['html']['css'],
			title='Tags / ' + tag_page.current.title,
			list=tag_page
			)
		filename = config['base_dir'] + '/dist/' + config['tags_dir'] + tag_page.key + '.html'
		write_file(filename, html)
	publish_tagcloud(config, data)

def generate_tags_list(config, data):
	tag_list = []
	prev_page = None
	for key in data:
		current_link = Link(key.replace('_',' '),  config['base_uri'] + config['tags_dir'] + key + '.html')
		prev_link = None
		if prev_page:
			prev_page.next = current_link
			prev_link = prev_page.current
		current_page = List(key, data[key], current_link, prev_link)
		tag_list.append(current_page)
		prev_page = current_page
	return tag_list

def publish_tagcloud(config, data):
	logger.info('Generating tagcloud page')
	max_count = 0
	for key in data:
		length = len(data[key])
		if max_count < length:
			max_count = length
	tags = []
	for key in data:
		length = len(data[key])
		size = ((length * 1.0)/max_count*30)+10
		tags.append(Tag(key.replace('_',' '),config['base_uri'] + config['tags_dir'] + key + '.html',size))
	template = get_template(config, 'tags.html')
	html = template.render(
			base_uri=config['base_uri'],
			js=config['html']['js'],
			css=config['html']['css'],
			title='Tags',
			tags=tags
			)
	filename = config['base_dir'] + '/dist/' + 'tags.html'
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

def publish_calendar(config, blogs):
	logger.debug('Generating calendar')
	year = collections.OrderedDict()
	month = collections.OrderedDict()
	date = collections.OrderedDict()
	for blog in blogs:
		item = Item(blog.current.href, blog.date, blog.title, blog.sub_title, blog.tags)
		y = str(blog.date.year)
		ym = y + '/' +two_digit(blog.date.month)
		ymd = ym + '/' + two_digit(blog.date.day)
		add_key_value(year, y, item)
		add_key_value(month, ym, item)
		add_key_value(date, ymd, item)
	publish_calendar_by(year, config)
	publish_calendar_by(month, config)
	publish_calendar_by(date, config)
	top = year.iterkeys().next()
	source = config['base_dir'] + '/dist/' + config['blogs_dir'] + top +'/index.html'
	dest = config['base_dir'] + '/dist/' + 'calendar.html'
	shutil.copyfile(source, dest)

def publish_calendar_by(data, config):
	template = get_template(config, 'list.html')
	for key in generate_calendar_list(config, data):
		html = template.render(
			base_uri=config['base_uri'],
			js=config['html']['js'],
			css=config['html']['css'],
			title=key.current.title,
			list=key			)
		filename = config['base_dir'] + '/dist/' + config['blogs_dir'] + key.key +'/index.html'
		write_file(filename, html)

def generate_calendar_list(config, data):
	calendar_list = []
	prev_page = None
	for key in data:
		current_link = Link( get_cal_title(key),  config['base_uri'] + config['blogs_dir'] + key + '/index.html')
		prev_link = None
		if prev_page:
			prev_page.next = current_link
			prev_link = prev_page.current
		current_page = List(key, data[key], current_link, prev_link)
		calendar_list.append(current_page)
		prev_page = current_page
	return calendar_list

def get_cal_title(title):
	cal = title.split('/')
	size = len(cal)
	if size == 1:
		return title
	elif size == 2:
		return months[int(cal[1])] + ' ' + cal[0]
	elif size == 3:
		return months[int(cal[1])] + ' ' + cal[2] + ', ' + cal[0]
	else:
		return title

def two_digit(number):
	if number > 9:
		return str(number)
	else:
		return '0' + str(number)

def add_key_value(data,key,value):
	if data.has_key(key):
		data[key] = [value] + data[key]
	else:
		data[key]=[value]