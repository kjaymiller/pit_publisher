from config import WEBSITE_URL, OWNER
from mongo import db
from datetime import datetime
from bson.objectid import ObjectId
from markdown import markdown
import pytz

def feed_param(k, val, cdata=False, *args):
    if cdata:
        return '<{0}><![CDATA[{1}]]></{0}>'.format(k, val)

    else:
        return '<{0}>{1}</{0}>'.format(k, val)


class Link():
    def __init__(self, url):
        self.url = url

class iTunes(Link):
    name = 'iTunes'
    image = 'http://productivityintech.com/files/images/Get_it_on_iTunes_Badge_US_1114.svg'

class Google(Link):
    name = 'Google'
    image = 'http://productivityintech.com/files/images/play_en_badge_web_generic.png'

class RSS(Link):
    name = 'RSS'
    image = 'http://productivityintech.com/files/images/rss.png'

class Collection():
    def __init__(self, title, collection, uuid, subtitle='',):
        self.title = title
        self.collection = db[collection]
        self.collection_name = collection
        self.subtitle = subtitle
        self.uuid = uuid

    def rss(self):
        updated_date = datetime.now(pytz.utc).isoformat()
        db_entries = self.collection.find({'published':True}).sort('publish_date', -1)
        rss_entries = ''

        # RSS Entries
        for d in db_entries:
            d_id = ObjectId(d['_id'])
            url = '{}/{}/{}'.format(WEBSITE_URL, self.collection_name, d_id)
            title = feed_param('title', d['title'])
            link = feed_param('link', url)
            id = feed_param('link', url)
            author = feed_param('author', feed_param('name',d['author']))
            content = feed_param('content', d['content'], cdata=True)
            updated = feed_param('updated', d['publish_date'])
            entry_data = ''.join((title, link, id, author, content, updated))
            rss_entry =feed_param('entry', entry_data)
            rss_entries += rss_entry

        # Full RSS File
        xmlns = '<feed xmlns="http://www.w3.org/2005/Atom">'
        rss_xml = '<?xml version="1.0" encoding="UTF-8"?>'
        title = feed_param.format('title', self.title)
        subtitle = feed_param('subtitle', self.subtitle)
        rss_link = '<link rel="self" type="application/atom+xml" href="{}/files/{}.xml" />'.format(WEBSITE_URL, self.collection_name)
        coll_link = '<link rel="alternate" type="text/html" hreflang="en" href="{}/{}" />'.format(WEBSITE_URL, self.collection_name)
        updated = feed_param('updated', updated_date)
        id = feed_param('id', 'uuid:{}'.format(self.uuid))
        feed_info = ''.join((xmlns,
                            rss_xml,
                            title,
                            subtitle,
                            rss_link,
                            coll_link,
                            updated,
                            id))
        feed = '{}{}</feed>'.format(feed_info, rss_entries)
        return rss_data

class Podcast(Collection):
    def __init__(self, title, uuid, links, collection, description, abbreviation,
                image_href, categories, keywords, subtitle, new_feed=None
                owner=OWNER):
        super().__init__(title=title, uuid=uuid, collection=collection, subtitle=subtitle)
        self.links = links
        self.description = description
        self.abbreviation = abbreviation
        self.owner = owner
        self.categories = categories
        self.keywords = keywords
        self.image_href = image_href
        if new_feed:
            self.new_feed=new_feed

    def rss(self, language='en', expl='no'):
        updated_date = datetime.now(pytz.utc).strftime('%a, %d %b %Y %H:%M:%S %z')
        db_entries = self.collection.find({'published':True}).sort('episode_number', -1)
        rss_entries = ''
        feed_url = '{}/files/{}.rss'.format(WEBSITE_URL, self.collection_name)
        podcast_url = '{}/{}'.format(WEBSITE_URL, self.collection_name)

        # RSS Entries
        for d in db_entries:
            print(d['episode_number'])
            abbr = self.abbreviation
            showtitle = '{} {}: {}'.format(abbr, d['episode_number'], d['title'])
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
            fields = (title, subtitle, enclosure, link, description, duration, pub_date, explicit, keywords)
            for field in fields:
                if not isinstance(field, str):
                    print(field)

            entry_data = '\n'.join(fields)
            rss_entry = feed_param('item', entry_data)
            rss_entries += rss_entry

        # Full RSS File
        rss_xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xmlns = '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:cc="http://web.resource.org/cc/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:media="http://search.yahoo.com/mrss/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'

        #channel Properties
        atom_link = '<atom:link href="" rel="self" type="application/rss+xml"/>'
        title = feed_param('title', self.title)
        pub_date = feed_param('pubDate', updated_date)
        last_build_date = feed_param('lastBuildDate', updated_date)
        generator = feed_param('generator', 'Productivity in Tech RSS Generator')
        link = feed_param('link', podcast_url)
        language = feed_param('language', language)
        docs = feed_param('docs', podcast_url)

        img_href = feed_param('url', self.image_href)
        img_link = feed_param('link', WEBSITE_URL, cdata=True)
        image = feed_param('image', ''.join((img_href, title, img_link)))

        author = feed_param('itunes:author', self.owner['name'])
        keywords = feed_param('itunes:keywords', ','.join(self.keywords))

        if self.new_feed:
            new_feed = feed_param('itunes:new-feed-url', self.new_feed)
        else:
            new_feed = '
            '
        categories = '\n'.join(['<itunes:category text="{}" />'.format(x) for x in self.categories])
        itunes_image = '<itunes:image href="{}" />'.format(self.image_href)
        explicit = feed_param('itunes:explicit', expl)

        own_name = feed_param('itunes:name', self.owner['name'])
        own_email = feed_param('itunes:email', self.owner['email'])
        owner = feed_param('itunes:owner', ''.join((own_name, own_email)))

        description = feed_param('description', self.description, cdata=True)
        subtitle = feed_param('itunes:subtitle', self.subtitle)
        fields = (title,
                pub_date,
                last_build_date,
                generator,
                link,
                language,
                docs,
                image,
                keywords,
                new_feed,
                categories,
                itunes_image,
                owner,
                description,
                subtitle,
                rss_entries)
        for field in fields:
                if not isinstance(field, str):
                    print(field)

        feed_info = '\n'.join(fields)
        channel = feed_param('channel', feed_info)
        rss_feed = '\n'.join((rss_xml, xmlns, channel, '</rss>'))
        return rss_feed
