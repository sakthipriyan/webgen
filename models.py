class Link:
  def __init__(self, *args, **kwargs):
    self.title = kwargs.get('title')
    self.href = kwargs.get('href')

class Tag:
  def __init__(self, *args, **kwargs):
    self.link = kwargs.get('link')
    self.last_used = kwargs.get('last_used')
    self.count = kwargs.get('count')

class Page(object):
  def __init__(self, *args, **kwargs):
    self.href = kwargs.get('href')
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
    self.img = kwargs.get('img')
    self.date = kwargs.get('date')
    self.content = kwargs.get('content')
    self.tags = kwargs.get('tags')
    self.prev = kwargs.get('prev')
    self.next = kwargs.get('next')

class CalendarPage(Page):
  def __init__(self, *args, **kwargs):
    super(CalendarPage, self).__init__(*args, **kwargs)
    self.year = kwargs.get('year')
    self.months = kwargs.get('months')
    self.recent_tags = kwargs.get('recent_tags')

class ListPage(Page):
  def __init__(self, *args, **kwargs):
    super(CalendarPage, self).__init__(*args, **kwargs)
    self.title = kwargs.get('title')
    self.sub_title = kwargs.get('sub_title')
    self.links = kwargs.get('links')
    self.prev = kwargs.get('prev')
    self.next = kwargs.get('next')