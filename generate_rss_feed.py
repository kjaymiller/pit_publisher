from config import RSS_LOCATION
from datetime import datetime
from ssh import ssh
import pytz


def update_published(podcast, episode_number=None):
    if episode_number:
        episodes = podcast.collection.find({'published': False,
                                            'episode_number': episode_number})
    else:
        episodes = podcast.collection.find({'published': False})

    for entry in episodes
        publish_format = '%a, %d %b %Y %H:%M:%S %z'
        publish_date = datetime.strptime(entry['publish_date'], publish_format)

        if publish_date < datetime.now(pytz.utc):
            podcast.collection.find_one_and_update(
                {'episode_number': entry['episode_number']},
                {'$set': {'published': True}})

    return podcast.rss()

def upload_rss(podcast, path=RSS_LOCATION):
    rss = podcast.rss()
    rss_path = '{}.rss'.format(podcast.collection_name)
    with open(rss_path, 'w') as f:
        f.write(rss)

    ssh(rss_path, RSS_LOCATION)
