from jinja2 import Environment, FileSystemLoader
from models import HomePage

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
	f = open(base + '/dist/' + md_path.replace('.md','.html'),'w')
	f.write(html)
	f.close()

generateBlog('/home/sakthipriyan/ws/blog/sakthipriyan.com','2015/03/12/first-blog-done.md')
