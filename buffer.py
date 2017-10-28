from config import BUFFER_TOKEN
import requests
token = BUFFER_TOKEN

def schedule_post(post, link, title):
    accounts = ('56caadde820f27212d9a37b9', '573b1c5d3d4c3fde2671aad3', '5902181f24e004d4333b773d')
    url = f'https://api.bufferapp.com/1/updates/create.json?access_token={token}'
    for profile in accounts:
        data = {'profile_ids':profile,
            'text': post + link,
            'media': {'link': link,
                    'title': title}}
        requests.post(url, data = data)
