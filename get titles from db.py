import csv
from podcasts import pitpodcast

episodes = pitpodcast.collection.find()
titles = [episode['title'] for episode in episodes]

with open('titles.csv', 'w') as f:
    writer = csv.writer(f)
    for line in titles:
        writer.writerow([line])
