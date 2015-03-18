from jinja2 import Environment, FileSystemLoader
from models import HomePage

def getEnvironment(path):
	return Environment(loader=FileSystemLoader(path))

env = getEnvironment('/home/sakthipriyan/ws/blog/sakthipriyan.com/web/html')
template = env.get_template('base.html')
homepage = HomePage(
	base = 'file:///home/sakthipriyan/ws/blog/sakthipriyan.com/dist',
    href = 'href',
    title = 'First Render',
    css = ['bootstrap.min.css','font-awesome.min.css','highlight-github.min.css','main.css'],
    js = ['bootstrap.min.js','highlight.min.js','jquery-1.11.2.min.js','main.js'])

html = template.render(data=homepage)

f = open('/home/sakthipriyan/ws/blog/sakthipriyan.com/dist/index.html','w')
f.write(html) # python will convert \n to os.linesep
f.close()