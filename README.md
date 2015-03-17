# static-web
Python project to generate static websites from markdown

#Goals

Create simple blog generator from markdown size.
Blog will have following pages.

a) Home page

b) Blog page

c) Calendar page (Yearly list of blog pages)

d) Tags page (List of tags used across the blog pages)

e) List page (To list blog pages by date, tags,etc.,)

#Data
```

#Page element, applicable for all pages
page (object)
  title (string)
  css (array(string))
  js (array(string))
  
link (object)
  title
  href

#Home
page (object)
last_blog (blog)
recent_blogs (array(link))
recent_tags (array(link))

#Blog
page (object)
blog (object)
  title (string)
  sub_title (string)
  img (string)
  date (string)
  content (string)
  tags (array(link))
  links
    prev (link)
    next (link)

#Calendar
page        (object)
calendar    (blog)
  year      (int)
  
#tags
tag
  link      (link)
  last_used (date)
  count     (int)
```
