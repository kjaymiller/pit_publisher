from podcasts import pitpodcast, pitreflections
from sys import argv
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from urllib.request import urlopen
from config import FILE_STORAGE_LOCATION 
import re
import pytz

p = argv[1]
collections = {'pitpodcast': pitpodcast, 'pitreflections':pitreflections}
podcast_name = p.split('_')[0]
episode_number = p.split('_')[1]
podcast = collections[podcast_name]

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect('productivityintech.com', username='pituser')

def header(val, text, delimit=False):
    re_chk = ': *(.*)$'
    r = re.search('^' + val + re_chk, text, re.I|re.M)

    if r:
        print(r.group(0) + ' found!')
        result = r.group(1)

        if delimit:
            return result.split(',')

        else:
            return result

    else:
        return ''

def strip_headers(text):
    index = 0

    while re.match(r'\w+: *(.*)', text.splitlines()[index]):
        index += 1

    content_lines = text.splitlines()[index:]
    return '\n'.join(content_lines)

UPLOAD_PATH = 'posts/'
mp3_path = UPLOAD_PATH + '{}.mp3'.format(p)
md_path = UPLOAD_PATH + '{}.md'.format(p)

print('Uploading {}  to {}' + (mp3_path, FILE_STORAGE_LOCATION)
with SCPClient(ssh.get_transport()) as scp:
    scp.put(mp3_path, FILE_STORAGE_LOCATION)

print('Analyzing ' + md_path)
with open(md_path) as f:
    from_file = f.read()

publish_format = '%a, %d %b %Y %H:%M:%S %z'
if len(argv) == 3:
    unformatted_date = argv[2]

else :
    unformatted_date = header('publish_date', text=from_file)

if unformatted_date:
    fmt = '%m%d%y %H%M'
    d = datetime.strptime(unformatted_date, fmt)
    publish_date = d.replace(tzinfo=pytz.utc).strftime(publish_format)

else:
    publish_date = datetime.now(pytz.utc).strftime(publish_format)

if datetime.strptime( publish_date, publish_format) < datetime.now(pytz.utc):
    published = True
else:
    published = False

title = header('title', text=from_file)
subtitle = header('subtitle', text=from_file)
author = header('author', text=from_file)
summary = header('summary', text=from_file)
tags = header('tags', text=from_file, delimit=True)
episode_number = int(header('episode_number', text=from_file))
media_url = header('media_url', text=from_file)
duration = header('duration', text=from_file)
content = strip_headers(from_file)
length = len(urlopen(media_url).read())

podcast.collection.insert_one({
        'title': title,
        'subtitle': subtitle,
        'author': author,
        'tags': tags,
        'duration': duration,
        'summary': summary,
        'publish_date': publish_date,
        'episode_number': episode_number,
        'media_url': media_url,
        'published': published,
        'length': length,
        'content': content})
