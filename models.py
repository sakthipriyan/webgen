import datetime

class Link:
  def __init__(self, *args, **kwargs):
    self.title = kwargs.get('title')
    self.href = kwargs.get('href')

class Tag:
  def __init__(self, *args, **kwargs):
    self.link = kwargs.get('link')
    self.last_used = kwargs.get('last_used')
    self.count = kwargs.get('count')

class LinkItem:
    def __init__(self, *args, **kwargs):
        self.date = kwargs.get('date')
        self.link = kwargs.get('link')
        self.title = kwargs.get('title')
        self.sub_title = kwargs.get('sub_title')    
        self.tags = kwargs.get('tags')

class Page(object):
  def __init__(self, *args, **kwargs):
    self.base = kwargs.get('base')
    self.title = kwargs.get('title')
    self.css = kwargs.get('css')
    self.js = kwargs.get('js')

class HomePage(Page):
  def __init__(self, *args, **kwargs):
    super(HomePage, self).__init__(*args, **kwargs)
    self.last_blog = kwargs.get('last_blog')
    self.recent_blogs = kwargs.get('recent_blogs')
    self.recent_tags = kwargs.get('recent_tags')

class BlogPage(Page):
  def __init__(self, *args, **kwargs):
    super(BlogPage, self).__init__(*args, **kwargs)
    self.title = kwargs.get('title')
    self.sub_title = kwargs.get('sub_title')
    self.date = kwargs.get('date')
    self.markdown = kwargs.get('markdown')
    self.html = kwargs.get('html')
    self.tags = kwargs.get('tags')
    self.prev = kwargs.get('prev')
    self.next = kwargs.get('next')

class ListPage(Page):
  def __init__(self, *args, **kwargs):
    super(ListPage, self).__init__(*args, **kwargs)
    self.link_items = kwargs.get('link_items') 
    self.prev = kwargs.get('prev')
    self.next = kwargs.get('next')

class BlogItem:
    def __init__(self, path):
        date_str = ''.join(path.split('/')[-4:-1])
        self.date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
        self.path = path    
    
    def __str__(self):
        return '(date=%s, path=%s)' % (self.date, self.path)

    def __repr__(self):
        return self.__str__()