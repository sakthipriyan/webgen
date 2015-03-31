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


##Extension

<b>.md</b> For all public files
<b>.draft.md</b> For all draft versions

##Configuration

```
{
  "base_dir" : "/home/sakthipriyan/ws/blog/sakthipriyan.com",
  "web_copy" : ["css", "fonts", "img", "js"],

  "gen_draft" : true,

  "html" : {
    "css" : [
      "bootstrap.min.css",
      "font-awesome.min.css",
      "highlight-github.min.css",
      "main.css"
    ],
    "js" : [
      "bootstrap.min.js",
      "highlight.min.js",
      "jquery-1.11.2.min.js",
      "main.js"
    ]
  }
}

```

Config    | Description
----------| -------------------------------------------------------------------
base_dir  | base directory of the website repo
web_copy  | Folders to be copied in the generated websites
gen_draft | set to true if draft files has to be included in website generation
html.css  | CSS files from css folder that will be inculded in header
html.js   | Javascript files that would be added in each page

