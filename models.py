self.from config import WEBSITE_URL, OWNER
from mongo import db
from datetime import datetime as dt
from markdown import markdown
import pytz


def feed_param(k, val, cdata=False, *args):
    if cdata:
        return '<{0}><![CDATA[{1}]]></{0}>'.format(k, val)

    else:
        return '<{0}>{1}</{0}>'.format(k, val)


class Collection():
    def __init__(self, title, collection, uuid, subtitle='',):
        self.title = title
        self.collection = db[collection]
        self.collection_name = collection
        self.subtitle = subtitle
        self.uuid = uuid


class Podcast(Collection):
    def __init__(
            self, title, uuid, collection, description, abbreviation,
            image_href, categories, keywords, subtitle, new_feed=None,
            owner=OWNER):

        super().__init__(
            title=title, uuid=uuid, collection=collection, subtitle=subtitle)

        self.description = description
        self.abbreviation = abbreviation
        self.owner = owner
        self.categories = categories
        self.keywords = keywords
        self.image_href = image_href
        self.new_feed = new_feed


def rss(podcast, language='en', expl='no'):
    updated_date = dt.now(pytz.utc).strftime('%a, %d %b %Y %H:%M:%S %z')
    publish = {'published': True}
    db_entries = self.collection'].find(publish).sort('episode_number', -1)
    rss_entries = ''
    podcast_url = '{}/{}'.format(WEBSITE_URL, self.collection_name'])

    # RSS Entries
    for d in db_entries:
        print(d['episode_number'])
        ab = d['abbreviation']
        showtitle = '{} {}: {}'.format(ab, d['episode_number'], d['title'])
        url = '{}/{}'.format(podcast_url, d['episode_number'])
        title = feed_param('title', showtitle)
        link = feed_param('link', url)
        enclosure_url = 'url="{}"'.format(d['media_url'])
        length = 'length="{}"'.format(d['length'])
        enclosure = '<enclosure {} {} type="audio/mpeg" ></enclosure>'.format(enclosure_url, length)
        description = feed_param('description', markdown(d['content']), cdata=True)
        subtitle = feed_param('itunes:subtitle', d['subtitle'], cdata=True)
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
    title = feed_param('title', self.'title'])
    pub_date = feed_param('pubDate', updated_date)
    last_build_date = feed_param('lastBuildDate', updated_date)
    generator = feed_param('generator', 'Productivity in Tech RSS Generator')
    link = feed_param('link', podcast_url)
    language = feed_param('language', language)
    docs = feed_param('docs', podcast_url)
    img_href = feed_param('url', self.image_href'])
    img_link = feed_param('link', WEBSITE_URL, cdata=True)
    image = feed_param('image', ''.join((img_href, title, img_link)))
    keywords = feed_param('itunes:keywords', ','.join(self.keywords']))

    if new_feed in podcast:
        new_feed = feed_param('itunes:new-feed-url', self.new_feed'])
    else:
        new_feed = ''
    categories = '\n'.join(['<itunes:category text="{}" />'.format(x) for x in self.categories'])
    itunes_image = '<itunes:image href="{}" />'.format(self.image_href'])
    explicit = feed_param('itunes:explicit', expl)

    own_name = feed_param('itunes:name', self.owner']['name'])
    own_email = feed_param('itunes:email', self.owner']['email'])
    owner = feed_param('itunes:owner', ''.join((own_name, own_email)))

    description = feed_param('description', self.description'], cdata=True)
    subtitle = feed_param('itunes:subtitle', subtitle)
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
