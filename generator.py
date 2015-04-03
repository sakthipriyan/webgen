from jinja2 import Environment, FileSystemLoader
from models import HomePage, BlogPage, Link
import logging
import collections
import markdown

logger = logging.getLogger(__name__)

def getEnvironment(path):
	return Environment(loader=FileSystemLoader(path))

def generateBlog(base,md_path):
	homepage = HomePage(
		base = 'file:///home/sakthipriyan/ws/blog/sakthipriyan.com/dist',
		href = 'href',
		title = 'First Render',
		css = ['bootstrap.min.css','font-awesome.min.css','highlight-github.min.css','main.css'],
		js = ['bootstrap.min.js','highlight.min.js','jquery-1.11.2.min.js','main.js'])

	env = getEnvironment(base + '/web/html')
	template = env.get_template('blog.html')
	html = template.render(data=homepage)
	filename = base + '/dist/' + md_path.replace('.md','.html')
	if not os.path.exists(os.path.dirname(filename)):
		os.makedirs(os.path.dirname(filename))
	with open(filename, "w") as f:
		f.write(html)
		f.close()

#generateBlog('/home/sakthipriyan/ws/blog/sakthipriyan.com','2015/03/12/first-blog-done.md')

def generateBlogs(blogs,config):
	generated_blogs = []
	for blog in blogs:
		file_path = config['base_dir'] + '/src/' + blog.path
		logger.debug('Processing file %s' % file_path)
		with open (file_path, "r") as md_file:
			content = md_file.readlines()
			if(len(content) < 4):
				logger.warn('File %s Contains less than 4 lines, skipping' % blog.path)
				continue
			generated_blogs.append(getBlogPage(config, content, blog))
	linkPrevNext(generated_blogs)
	data = publishBlogs(config, generated_blogs)
	publishCalendar(config, data)
	publishTags(config, data)


def publishBlogs(config, generated_blogs):
	pass

def publishCalendar(config, data):
	pass

def publishTags(config, data):
	pass

def linkPrevNext(generated_blogs):
	prevBlog = None
	nextBlog = None
	for index, currentBlog in enumerate(generated_blogs):
		if(len(generated_blogs) > index + 1):
			nextBlog = generated_blogs[index+1]
		else:
			nextBlog = None
		if prevBlog is not None:
			currentBlog.prev = Link(prevBlog.title, prevBlog.href)
		if nextBlog is not None:
			currentBlog.next = Link(nextBlog.title, nextBlog.href)
		prevBlog = currentBlog

def getBlogPage(config, content, blog):
	title = content[0].strip()
	sub_title = content[1].strip()
	tags =  [s.strip() for s in content[2].split(',')]
	md = ''.join(content[3:])
	html = markdown.markdown(md)
	href = config['base_uri'] + config['blogs_dir'] + blog.path.replace('.md','.html')
	return BlogPage(title=title, sub_title=sub_title, date=blog.date, markdown=md,html=html,tags=tags, href=href)

def generateCalendar(blogs,config):
	logger.debug('Generating calendar')
	count = 0
	calendar = {}
	for blog in blogs:
		y = str(blog.date.year)
		ym = y + two_digit(blog.date.month)
		ymd = ym + two_digit(blog.date.day)
		addToDictArray(calendar, y, blog)
		addToDictArray(calendar, ym, blog)
		addToDictArray(calendar, ymd, blog)

	od = collections.OrderedDict(sorted(calendar.items()))
	logger.debug('%s pages generated for calendar' % count)

def two_digit(number):
	if number > 9:
		return str(number)
	else:
		return '0' + str(number)

def addToDictArray(dictArray,key,value):
	if dictArray.has_key(key):
		dictArray[key].append(value)
	else:
		dictArray[key]=[value]