from config import (WEBSITE_URL,
                    OWNER,
                    AUTHORS,
                    FEED_LOCATION,
                    GENERATOR_NAME,
                    GENERATOR_URI,
                    FEED_COPYRIGHT,
                    FEED_ICON,
                    FEED_LOGO,
                    FILES_PATH,
                    DEFAULT_UPLOAD_SOURCE)

from datetime import datetime
from markdown import markdown
from mongo import db, auth
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

generator = feed_param('generator', GENERATOR_NAME)

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
    if date <= datetime.now(pytz.utc):
        return True
    else:
        return False

publish_format = '%a, %d %b %Y %H:%M:%S %z'

def get_html_url(content):
    """Takes a HTML tag and returns the href or SRC"""
    href_q = re.search(r'<a.+href="(.+)">(.+)</a>', content)
    src_q = re.search(r'src="(.+)"', content)
    src_alt_q = re.search(r'src=.+alt=(".+").*>', content)

    if href_q:
        return href_q.group(1), href_q.group(2)
    elif src_q and src_alt_q:
        return src_q.group(1), src_alt_q.group(1)
    elif src_q and not src_alt_q:
        return src_q.group(1), ''

    else:
        return

def remove_iframes(content):
    q = re.search(r'<div.*><iframe.+</iframe></div>', content)
    q.group(0)

class Collection():
    def __init__(self, title, collection, uuid,):
        auth
        self.title = title
        self.collection = db[collection]
        self.collection_name = collection
        self.uuid = uuid

    def set_publish_date(self, pub_date):
        if pub_date:
            return datetime.strptime(pub_date, publish_format)
        else:
            return datetime.now(pytz.utc)


    def get_file_content(self, file_data):
        with open(file_data) as f:
            text = f.read()
        rows= text.splitlines()
        index = 0
        header = {}

        while re.search(r'^(\w+): *(.*)$', rows[index]):
            match = re.search(r'^(\w+): *(.*)$', rows[index])
            key = match.group(1).lower()
            val = match.group(2)

            if key == 'tags':
                val = val.split(',')
            header[key] = val
            index += 1

        # Use the rest of the content as the content value
        content_lines = rows[index:]
        header['content'] = '\n'.join(content_lines)

        #populate publish date if not present
        pub_date = self.set_publish_date(header.get('publish_date', ''))
        header['publish_date'] = pub_date
        return header

    def upload(self, headers):
        return self.collection.insert_one(headers)


class Blog(Collection):
    def __init__(
            self, title, uuid, collection, **kwargs):
        super().__init__(title=title, uuid=uuid, collection=collection)
        self.subtitle = kwargs.get('subtitle', None)

    def get_file_content(self, file_data):
        header = super().get_file_content(file_data)
        header['author'] = AUTHORS[header.get('author', 'OWNER')]
        return super().upload(header)

    def atom(self):
        #feed properties
        atom_date_fmt = '%Y-%m-%dT%H:%M:%S'
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
        link = f'<link rel="self" href="{WEBSITE_URL}/{FEED_LOCATION}" />'
        icon = feed_param('icon', FEED_ICON)
        logo = feed_param('logo', FEED_LOGO)
        rights = feed_param('rights', FEED_COPYRIGHT)
        atom_feed_info = f'''{rss_xml}
{xmlns}
{feed_id}
{link}
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

    def upload_podcast_episode(self, episode_file, shownotes=None, episode_number='',
                title=None, tags=None, publish_date=None):

        if not title:
            title = input("Title: ")

        if not tags:
            tags = input("Tags (comma separated): ").split(',')

        if not publish_date:
            pd_input = input("Publish Date (leave blank for NOW): ")
            publish_date = self.set_publish_date(pd_input)

        if shownotes:
            with open(shownotes) as f:
                content = f.read()
        else:
            content = title


        with open(episode_file, 'rb') as f:
            length = len(f.read())

        duration = get_duration(episode_file)
        episode_file_name = episode_file.split('/', 1)[1]
        header = {
            'title': title,
            'tags': tags,
            'publish_date': publish_date,
            'content': content,
            'duration': duration,
            'published': published(publish_date),
            'length': length,
            'media_url': f'{WEBSITE_URL}/{FILES_PATH}/podcast/{episode_file_name}'
            }
        if episode_number:
            header['episode_number'] = int(episode_number)

        else:
            header['episode_number'] = None

        return super().upload(header)


    def get_file_content(self, shownotes, episode_file):
        header = super().get_file_content(shownotes)
        with open(episode_file, 'rb') as f:
            header['length'] = len(f.read())
        header['duration'] = get_duration(episode_file)
        return super().upload(header)

    def rss(self, language='en', expl='no'):
        rss_date_format = '%a, %d %b %Y %H:%M:%S'
        updated_date = datetime.now(pytz.utc).strftime(rss_date_format)
        db_entries = self.collection.find().sort('publish_date', -1)
        rss_entries = ''
        podcast_url = f'{WEBSITE_URL}/{self.collection_name}'

        # RSS Entries
        for d in db_entries:
            showtitle = d['title']
            url=WEBSITE_URL

            url = f'{podcast_url}/{d["_id"]}'
            title = feed_param('title', showtitle)
            link = feed_param('link', url)
            enclosure_url = f"url=\"{d['media_url']}\""
            length = f"length=\"{d['length']}\""
            enclosure = f'<enclosure {enclosure_url} {length} type="audio/mpeg" ></enclosure>'
            description = feed_param('description', markdown(d['content']), cdata=True)
            subtitle = feed_param('itunes:subtitle', d.get('subtitle',''), cdata=True)
            duration = feed_param('itunes:duration', d['duration'])
            format_date = datetime.strftime(d['publish_date'], rss_date_format) #Convert to RSS Approved Date
            pub_date = feed_param('pubDate', format_date + ' +0000')
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
        pub_date = feed_param('pubDate', updated_date + ' +0000')
        last_build_date = feed_param('lastBuildDate', updated_date + ' +0000')
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
