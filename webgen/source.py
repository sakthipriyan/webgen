import os

def listBlogs(src):
	blogs = []
	for year in os.listdir(src):
		year_dir = src + '/' + year
		for month in os.listdir(year_dir):
			month_dir = year_dir + '/' + month
			for day in os.listdir(month_dir):
				day_dir = month_dir + '/' + day
				for article in os.listdir(day_dir):
					article_path = day_dir + '/' + article
					blogs.append(article_path)
	return blogs
