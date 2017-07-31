"""
Edit Podcast Shownotes
created: 21 Jun 2017
Author: Jay Miller @kjaymiller

Description:
The following file downloads the requested shownotes and replaces it with the modified version
Special Thanks to @ChrisWaterguy for pointing out the issue that made me write this! Long time coming, thanks Chris for being the straw that broke the camel's back.

example `python edit_shownotes.py some_podcast 42`
"""

from config import DEFAULT_UPLOAD_SOURCE
from sys import argv
from podcasts import podcasts

podcast = podcasts[argv[1]]
episode_number = int(argv[2])

# Download the file to be edited
episode = podcast.collection.find_one({'episode_number': episode_number})
shownotes = episode['content']
file_name = f"{podcast.collection_name}_{episode_number}.md"
file_path = f'{DEFAULT_UPLOAD_SOURCE}/{file_name}'

with open(file_path, 'w') as f:
    f.write(shownotes)

# pause and wait for enter
phrase = """Enter 'q' or 'quit' and press return[Enter] to exit.
The file will not be removed from your computer: """
if input(phrase).lower() not in ('quit', 'q'):
    with open(file_path, 'r') as f:
        f = f.read()
        podcast.collection.find_one_and_update(
            {'episode_number': episode_number},
            {'$set': {'content': f}})
