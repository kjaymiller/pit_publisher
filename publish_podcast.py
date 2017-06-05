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
from podcasts import podcasts

podcast_index = argv[1].split('_')
episode_number = int(podcast_index[1])
podcast_name = podcast_index[0].lower()
podcast = podcasts[podcast_name]
base_file = f'{DEFAULT_UPLOAD_SOURCE}'
mp3 = f'{base_file}/{argv[1]}.mp3'
md = f'{base_file}/{argv[1]}.md'
podcast.get_file_content(md, mp3, episode_number)

with open(f'{podcast_name}.rss', 'w') as f:
    f.write(podcast.rss())
