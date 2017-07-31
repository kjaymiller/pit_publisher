from sys import argv
from podcasts import podcasts

if argv[1] in podcasts.keys():
    podcast = podcasts[argv[1]]

    if len(argv) > 2:
        episode_number = argv[2]

    else:
        episode_number = ''

    podcast_name = argv[1]

if len(argv) > 2:
    podcast_prefix = f'{podcast_name}_{episode_number}'
else:
    podcast_prefix = input('Enter the File Name: ')

episode = f'{podcast_prefix}.mp3'
shownotes = f'{podcast_prefix}.md'
podcast.upload_podcast_episode(shownotes, episode, episode_number)

with open(f'{argv[1]}.rss', 'w') as f:
    f.write(podcast.rss())
