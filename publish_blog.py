"""
This is a quick way to upload your podcast.
In order to use PodcastUpload.py, the following information needs to be true:

* Your shownotes file needs to be named after the podcast collection_name
followed by an underscore and the episode number.
* Your podcast episode file needs to follow the same naming convention as the
shownotes.
* Your podcast must be an mp3 (chapterized is okay)

Your rss file will export in the root of the podcast upload directory
"""

from config import DEFAULT_UPLOAD_SOURCE
from sys import argv
from blog import blog

base_file = f'{DEFAULT_UPLOAD_SOURCE}'
md = f'{argv[1]}'
blog.get_file_content(md)

with open('feed.xml', 'w') as f:
    f.write(blog.atom())
