from sys import argv
from tweet import tweet

#starting with path_to_glory/podcast_1.md

basename = argv[1].split('/')[-1].split('.')[0].split('_') #[podcast,1]
episode_number = int(basename.pop(-1))
podcast = '_'.join(basename)

insert_episode = (podcast, argv[1], episode_number)
tweet()
