from tweet import tweet
from sys import argv
from podcasts import podcasts
import re

podcast = podcasts[argv[1]]
episode_number = int(argv[2])
print(tweet(podcast, episode_number))
