from podcasts import pitpodcast, pitreflections
from datetime import datetime
import pytz
from podcasts import podcasts
from sys import argv

if len(argv) == 2:
    casts = [argv[1]]
else:
    casts = podcasts

for p in casts:
    podcast = podcasts[p]
    print(podcast.title)
    for entry in podcast.collection.find({'published': False}):
        publish_format = '%a, %d %b %Y %H:%M:%S %z'
        publish_date = datetime.strptime(entry['publish_date'], publish_format)

        if publish_date < datetime.now(pytz.utc):
            podcast.collection.find_one_and_update({'episode_number': entry['episode_number']}, {'$set':{'published': True}}) 
            
    rss = podcast.rss()
    rss_path = '{}.rss'.format(podcast.collection_name)

    with open(rss_path, "w") as f:
        f.write(rss)
