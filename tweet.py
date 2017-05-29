def tweet(podcast, episode_number):
    collection = podcast.collection
    episode = collection.find_one({'episode_number': episode_number})
    url = f'http://productivityintech.com/{podcast.collection_name}/{episode_number}'
    title = episode['title']
    return f'New #{podcast.title} {episode_number}: {title} {url}'
