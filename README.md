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
#Common objects
page    (object)
  href  (string)
  title (string)
  css   (array(string))
  js    (array(string))

link    (object)
  title (string)
  href  (string)

#Home page
page            (object)
home            (object)
  last_blog     (blog)
  recent_blogs  (array(link))
  recent_tags   (array(link))

#Blog page
page          (object)
blog          (object)
  title       (string)
  sub_title   (string)
  img         (link)
  date        (date)
  content     (string)
  tags        (array(link))
  prev        (link)
  next        (link)

#Calendar
page        (object)
calendar    (object)
  year      (int)
  month     (dict(month:array(link)))

#Tags
page        (object)
tag         (object)
  link      (link)
  last_used (date)
  count     (int)

#List
page          (object)
list          (object)
  title       (string)
  sub_title   (string)
  links       (array(link))
  prev        (link)
  next        (link)
```
