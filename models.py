class Link:
  def __init__(self, title, href):
    self.title = title
    self.href = href
  def __str__(self):
    return '(title:%s, href:%s)' % (self.title, self.href)
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

class HomePage:
  def __init__(self, *args, **kwargs):
    self.url = kwargs.get('url')
    self.last_blog = kwargs.get('last_blog')
    self.recent_blogs = kwargs.get('recent_blogs')
    self.recent_tags = kwargs.get('recent_tags')

class Blog:
  def __init__(self, *args, **kwargs):
    self.path = kwargs.get('path')
    self.title = kwargs.get('title')
    self.sub_title = kwargs.get('sub_title')
    self.date = kwargs.get('date')
    self.html = kwargs.get('html')
    self.tags = kwargs.get('tags')
    self.current = kwargs.get('current')
    self.prev = kwargs.get('prev')
    self.next = kwargs.get('next')
  def __str__(self):
    return '\nBlog(\npath:%s\ntitle:%s\nsub_title:%s\ndate:%s\nhtml length:%s\ntags:%s\ncurrent:%s\nprev:%s\nnext:%s\n)' % (
        self.path, self.title, self.sub_title, self.date, len(self.html), self.tags, self.current, self.prev, self.next)
  def __repr__(self):
    return self.__str__()

class ListPage:
  def __init__(self, *args, **kwargs):
    super(ListPage, self).__init__(*args, **kwargs)
    self.link_items = kwargs.get('link_items') 
    self.prev = kwargs.get('prev')
    self.next = kwargs.get('next')

# class BlogItem:
#     def __init__(self, path):
#         date_str = ''.join(path.split('/')[-4:-1])
#         self.date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
#         self.path = path    
#     def __str__(self):
#         return '(date=%s, path=%s)' % (self.date, self.path)
#     def __repr__(self):
#         return self.__str__()
