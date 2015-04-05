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

class List:
    def __init__(self, title, items, prev_link, next_link):
        self.title = title
        self.items = items
        self.prev = prev_link
        self.next = next_link

class Item:
    def __init__(self, date, title, sub_title, tags):
        self.date = date
        self.title = title
        self.sub_title = sub_title
        self.tags = tags

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
