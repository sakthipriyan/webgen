import datetime

class Link:
  def __init__(self, title, href):
    self.title = title
    self.href = href
  def __str__(self):
    return '(title=%s, href=%s)' % (self.title, self.href)
  def __repr__(self):
    return self.__str__()

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
    self.url = kwargs.get('url')
    

class HomePage(Page):
  def __init__(self, *args, **kwargs):
    super(HomePage, self).__init__(*args, **kwargs)
    self.last_blog = kwargs.get('last_blog')
    self.recent_blogs = kwargs.get('recent_blogs')
    self.recent_tags = kwargs.get('recent_tags')

class BlogPage:
  def __init__(self, *args, **kwargs):
    self.title = kwargs.get('title')
    self.sub_title = kwargs.get('sub_title')
    self.date = kwargs.get('date')
    self.markdown = kwargs.get('markdown')
    self.html = kwargs.get('html')
    self.tags = kwargs.get('tags')
    self.href = kwargs.get('href')
    self.prev = kwargs.get('prev')
    self.next = kwargs.get('next')
  def __str__(self):
    return 'BlogPage(\ntitle:%s\nsub_title:%s\ndate:%s\nmarkdown:%s\nhtml:%s\ntags:%s\nhref:%s\nprev:%s\nnext:%s\n)' % (self.title, self.sub_title, self.date, None, None, self.tags, self.href, self.prev, self.next)

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

