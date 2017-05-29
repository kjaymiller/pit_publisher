from mutagen.mp3 import MP3
from datetime import datetime
import re
import pytz




def get_duration(mp3):
    audio = MP3(mp3)
    total_in_seconds = audio.info.length
    minutes = str(int(total_in_seconds/60))
    seconds = str(int(total_in_seconds%60))
    return minutes + ":" + seconds

def generate_headers(text):
    index = 0
    headers = {}
    rows=text.splitlines()
    while re.search(r'^(\w+): *(.*)$', rows[index]):
        match = re.search(r'^(\w+): *(.*)$', rows[index])
        key = match.group(1)
        val = match.group(2)

        if ';' in val:
            val = val.split(';')
        headers[key] = val
        index += 1

    # Use the rest of the content as the content value
    content_lines = text.splitlines()[index:]
    headers['content'] = '\n'.join(content_lines)

    #populate publish date if not present
    now = datetime.now(pytz.utc).strftime(publish_format)
    headers['publish_date'] = headers.get('publish_date', now)
    headers['published'] = published(headers['publish_date'])
    return headers
