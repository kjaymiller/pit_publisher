from config import AUTHORS, OWNER
from sys import argv
from blog import blog

file_path = argv[1]
title = input("Title: ")
tags = input("Tags (comma separated): ").split(',')
author = input("Author (leave blank for site OWNER): ")
pub_date = input("Publish Date (leave blank for NOW): ")
featured_image = input("Featured Image (URL): ")

with open(file_path) as f:
    content = f.read()

header = {'title': title,
          'tags': tags,
          'content': content,
          'featured_image': featured_image,
          'published': True}

# Add Author
if author:
    header['author'] = AUTHORS[author]
else:
    header['author'] = OWNER
# Add Publish_Date
    header['publish_date'] = blog.set_publish_date(pub_date)

blog.upload(header)
