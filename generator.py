from jinja2 import Environment, FileSystemLoader
from models import HomePage
import logging
import collections

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
	prevBlog = None
	nextBlog = None
	for index, currentBlog in enumerate(blogs):
		if(len(blogs) > index + 1):
			nextBlog = blogs[index+1]
		else:
			nextBlog = None
		print prevBlog, currentBlog, nextBlog
		prevBlog = currentBlog


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
	print od

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
