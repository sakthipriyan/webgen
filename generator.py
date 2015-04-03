from jinja2 import Environment, FileSystemLoader
from models import HomePage, BlogPage
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
	data = {}
	base_uri = config['base_uri']
	blog_dir = config['blogs_dir']
	for blog in blogs:
		file_path = config['base_dir'] + '/src/' + blog.path
		logger.debug('Processing file %s' % file_path)
		with open (file_path, "r") as md_file:
			content = md_file.readlines()
			if(len(content) < 4):
				logger.warn('File %s Contains less than 4 lines, skipping' % blog.path)
				continue
			title = content[0].strip()
			sub_title = content[1].strip()
			tags =  [s.strip() for s in content[2].split(',')]
			md = ''.join(content[3:])
			html = markdown.markdown(md)
			url = config['base_uri'] + config['blogs_dir'] + blog.path.replace('.md','.html')
			generated_blogs.append(BlogPage(title=title, sub_title=sub_title, date=blog.date, markdown=md,html=html,tags=tags, url=url))
  
			logger.debug('Title : %s', title)
			logger.debug('Sub Title : %s', sub_title)
			logger.debug('date : %s', blog.date)
			logger.debug('Tags : %s', tags)
			logger.debug('Markdown : %s', md)
			logger.debug('HTML : %s', html)
			logger.debug('url : %s', url)


	print generated_blogs

	#	break

		
	# prevBlog = None
	# nextBlog = None
	# for index, currentBlog in enumerate(blogs):
	# 	if(len(blogs) > index + 1):
	# 		nextBlog = blogs[index+1]
	# 	else:
	# 		nextBlog = None
	# 	print prevBlog, currentBlog, nextBlog
	# 	prevBlog = currentBlog


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
