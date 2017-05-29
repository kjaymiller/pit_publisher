from config import WEBSITE_URL, OWNER, AUTHORS
from config import (
    FEED_LOCATION,
    GENERATOR_NAME,
    GENERATOR_URI,
    FEED_COPYRIGHT,
    FEED_ICON,
    FEED_LOGO)
from datetime import datetime
from markdown import markdown
from mongo import db
from mutagen.mp3 import MP3
import pytz
import re


def feed_param(key, value, cdata=False, xhtml=False, uri=None):
    if cdata:
        return f'<{key}><![CDATA[{value}]]></{key}>'

    elif xhtml:
        xhtml_url = 'http://www.w3.org/1999/xhtml'
        return f'''<{key} type="xhtml">
  <div xmlns="{xhtml_url}">
    {value}
  </div>
</{key}>'''

    elif uri:
        return f'''<{key} uri="{uri}">
  {value}
</{key}>'''

    else:
        return f'<{key}>{value}</{key}>'

generator = feed_param('generator', GENERATOR_NAME, uri=GENERATOR_URI)

def get_duration(mp3):
    audio = MP3(mp3)
    total_in_seconds = audio.info.length
    minutes = str(int(total_in_seconds/60))
    seconds = str(int(total_in_seconds%60))
    return minutes + ":" + seconds


def author_entry(author):
    return f'''<author>
<name>{author["name"]}</name>
<email>{author["email"]}</email>
<uri>{author["uri"]}</uri>
</author>'''


def published(date):
    if date <= datetime.now()):
        return True
    else:
        return False

publish_format = '%a, %d %b %Y %H:%M:%S %z'


class Collection():
    def __init__(self, title, collection, uuid,):
        self.title = title
        self.collection = db[collection]
        self.collection_name = collection
        self.uuid = uuid

    def get_file_content(self, file_data):
        with open(file_data) as f:
            text = f.read()
        rows= text.splitlines()
        index = 0
        header = {}

        while re.search(r'^(\w+): *(.*)$', rows[index]):
            match = re.search(r'^(\w+): *(.*)$', rows[index])
            key = match.group(1)
            val = match.group(2)

            if ';' in val:
                val = val.split(';')
            header[key] = val
            index += 1

        # Use the rest of the content as the content value
        content_lines = rows[index:]
        header['content'] = '\n'.join(content_lines)

        #populate publish date if not present
        now = datetime.now(pytz.utc).strftime(publish_format)
        header['publish_date'] = header.get('publish_date', now)
        header['published'] = published(header['publish_date'])
        return header

    def update_published(self, val, attr="_id"):
        entries = podcast.collection.find({'published': False})
        for entry in entries:
            if episode.published_date >= datetime.now():
                podcast.collection.update_one(
                        {'episode_number', episode['episode_number']},
                        {'$set':{published: True}})
        return entries

    def upload(self, headers):
        return self.collection.insert_one(headers)


class Blog(Collection):
    def __init__(
            self, title, uuid, collection, default_author=OWNER, **kwargs):
        super().__init__(title=title, uuid=uuid, collection=collection)
        self.default_author=OWNER
        self.subtitle = kwargs.get('subtitle', None)

    def get_file_content(self, file_data):
        header = super().get_file_content(file_data)
        header['author'] = AUTHORS[header.get('author', 'OWNER')]
        return header

    def atom(self):
        #feed properties
        atom_date_fmt = '%Y-%m-%dT%H:%M:%SZ'
        updated_date = datetime.now(pytz.utc).strftime(atom_date_fmt)
        rss_xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xmlns = '<feed xmlns= "http://www.w3.org/2005/Atom">'
        feed_author = author_entry(OWNER)
        updated = feed_param('updated', updated_date)
        title = feed_param('title', self.title)
        feed_id =  feed_param('id', f'urn:uuid:{self.uuid}')

        if self.subtitle:
            subtitle = feed_param('subtitle', self.subtitle)
        else:
            subtitle = ''
        link = f'<link rel="self" href="{FEED_LOCATION}" />'
        icon = feed_param('icon', FEED_ICON)
        logo = feed_param('logo', FEED_LOGO)
        rights = feed_param('rights', FEED_COPYRIGHT)
        atom_feed_info = f'''{rss_xml}
{xmlns}
{feed_id}
{feed_author}
{updated}
{title}
{subtitle}
{icon}
{logo}
{generator}
{rights}'''

        entries = []
        for entry in self.collection.find({}, sort=[('publish_date', -1)]):
            item_id = entry["_id"]
            entry_url = f'{WEBSITE_URL}/blog/{item_id}'
            entry_id = feed_param('id', entry_url)
            entry_title = feed_param('title', entry['title'])

            # Update Field Setup
            updated_date = entry['publish_date']
            fmt_updated_date = datetime.strftime(updated_date, atom_date_fmt)
            updated = feed_param('updated', fmt_updated_date)

            author = author_entry(entry['author'])
            html_content = markdown(entry['content'])
            content = feed_param('content', html_content, xhtml=True)
            link = f'<link rel="alternate" href="{entry_url}" />'

            entries.append(f'''<entry>
  {entry_id}
  {entry_title}
  {updated}
  {author}
  {content}
  {link}
</entry>''')

        entries = '\n'.join(entries)
        return f'{atom_feed_info}\n{entries}\n</feed>'

class Podcast(Collection):
    def __init__(
            self, title, uuid, collection, description, abbreviation,
            image_href, categories, keywords, new_feed=None,
            owner=OWNER, subtitle=''):

        super().__init__(title=title, uuid=uuid, collection=collection)

        self.description = description
        self.abbreviation = abbreviation
        self.owner = owner
        self.categories = categories
        self.keywords = keywords
        self.image_href = image_href
        self.new_feed = new_feed
        self.subtitle = subtitle


    def get_file_content(self, shownotes, episode_file, episode_number):
        header = super().get_file_content(shownotes)
        with open(episode_file, 'rb') as f:
            header['length'] = len(f.read())

        header['duration'] = get_duration(episode_file)
        episode_number = header.get('episode_number', episode_number)
        header['episode_number'] = int(episode_number)
        header['published'] = published(header['publish_date'])
        return super().upload(header)


    def rss(self, language='en', expl='no'):
        rss_date_format = '%a, %d %b %Y %H:%M:%S %z'
        updated_date = datetime.now(pytz.utc).strftime(rss_date_format)
        publish = {'published': True}
        db_entries = self.collection.find(publish).sort('episode_number', -1)
        rss_entries = ''
        podcast_url = '{}/{}'.format(WEBSITE_URL, self.collection_name)

        # RSS Entries
        for d in db_entries:
            ab = self.abbreviation
            showtitle = '{} {}: {}'.format(ab, d['episode_number'], d['title'])
            url = '{}/{}'.format(podcast_url, d['episode_number'])
            title = feed_param('title', showtitle)
            link = feed_param('link', url)
            enclosure_url = 'url="{}"'.format(d['media_url'])
            length = 'length="{}"'.format(d['length'])
            enclosure = '<enclosure {} {} type="audio/mpeg" ></enclosure>'.format(enclosure_url, length)
            description = feed_param('description', markdown(d['content']), cdata=True)
            subtitle = feed_param('itunes:subtitle', d.get('subtitle',''), cdata=True)
            duration = feed_param('itunes:duration', d['duration'])
            pub_date = feed_param('pubDate', d['publish_date'])
            explicit = feed_param('itunes:explicit', expl)
            keywords = feed_param('itunes:keywords', ','.join(d['tags']))
            fields = (
                title, subtitle, enclosure, link, description, duration,
                pub_date, explicit, keywords)

            for field in fields:
                if not isinstance(field, str):
                    print(field)

            entry_data = '\n'.join(fields)
            rss_entry = feed_param('item', entry_data)
            rss_entries += rss_entry

        # Full RSS File
        rss_xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xmlns = '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:cc="http://web.resource.org/cc/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:media="http://search.yahoo.com/mrss/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'

        # channel Properties
        title = feed_param('title', self.title)
        pub_date = feed_param('pubDate', updated_date)
        last_build_date = feed_param('lastBuildDate', updated_date)
        link = feed_param('link', podcast_url)
        language = feed_param('language', language)
        docs = feed_param('docs', podcast_url)
        img_href = feed_param('url', self.image_href)
        img_link = feed_param('link', WEBSITE_URL, cdata=True)
        image = feed_param('image', ''.join((img_href, title, img_link)))
        keywords = feed_param('itunes:keywords', ','.join(self.keywords))

        if self.new_feed:
            new_feed = feed_param('itunes:new-feed-url', self.new_feed)
        else:
            new_feed = ''
        categories = '\n'.join(['<itunes:category text="{}" />'.format(x) for x in self.categories])
        itunes_image = '<itunes:image href="{}" />'.format(self.image_href)
        explicit = feed_param('itunes:explicit', expl)

        own_name = feed_param('itunes:name', self.owner['name'])
        own_email = feed_param('itunes:email', self.owner['email'])
        owner = feed_param('itunes:owner', ''.join((own_name, own_email)))

        description = feed_param('description', self.description, cdata=True)
        subtitle = feed_param('itunes:subtitle', self.subtitle)
        fields = (
            title, pub_date, last_build_date, generator, link, language, docs,
            image, keywords, new_feed, categories, itunes_image, owner,
            description, subtitle, rss_entries)

        for field in fields:
                if not isinstance(field, str):
                    print(field)

        feed_info = '\n'.join(fields)
        channel = feed_param('channel', feed_info)
        rss_feed = '\n'.join((rss_xml, xmlns, channel, '</rss>'))
        return rss_feed
