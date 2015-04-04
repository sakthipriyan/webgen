from jinja2 import Environment, FileSystemLoader
from models import HomePage, Blog, Link
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
	data = publish_blogs(config, generated_blogs)
	# publishCalendar(config, data)
	# publishTags(config, data)

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
		link = Link(tag,  config['base_uri'] + config['tags_dir'] + tag.replace(' ', '_') + '.html')
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

def publish_blogs(config, generated_blogs):
	data = {}
	for blog in generated_blogs:
		base_dir = config['base_dir']
		env = getEnvironment(base_dir + '/web/html')
		template = env.get_template('blog.html')
		html = template.render(
			js=config['html']['js'], 
			css=config['html']['css'], 
			title=blog.title,
			data=blog, 
			base_uri=config['base_uri'])
		filename = base_dir + '/dist/' + config['blogs_dir'] + blog.path
		print filename
		if not os.path.exists(os.path.dirname(filename)):
			os.makedirs(os.path.dirname(filename))
		with open(filename, "w") as f:
			f.write(html)
			f.close()

	return data


# Blog(
# path:2015/04/01/gitconfig-alias.html
# title:Git Configuration Short hand
# sub_title:Alias for generally used Git commands
# date:2015-04-01
# html length:321
# tags:[(title:git, href:file:///home/sakthipriyan/workspace/blog/sakthipriyan.com/dist/tags/git.html), (title:config, href:file:///home/sakthipriyan/workspace/blog/sakthipriyan.com/dist/tags/config.html), (title:version control, href:file:///home/sakthipriyan/workspace/blog/sakthipriyan.com/dist/tags/version_control.html), (title:.gitconfig, href:file:///home/sakthipriyan/workspace/blog/sakthipriyan.com/dist/tags/.gitconfig.html), (title:setup, href:file:///home/sakthipriyan/workspace/blog/sakthipriyan.com/dist/tags/setup.html)]
# current:(title:Git Configuration Short hand, href:file:///home/sakthipriyan/workspace/blog/sakthipriyan.com/dist/blogs/2015/04/01/gitconfig-alias.html)
# prev:(title:Falcon set up, href:file:///home/sakthipriyan/workspace/blog/sakthipriyan.com/dist/blogs/2015/03/31/falcon-setup.html)
# next:None
# )















def getEnvironment(path):
	return Environment(loader=FileSystemLoader(path))

#generateBlog('/home/sakthipriyan/ws/blog/sakthipriyan.com','2015/03/12/first-blog-done.md')

def generate(blogs,config):
	pass

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
		dictArray[key].append(value)
	else:
		dictArray[key]=[value]