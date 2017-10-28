import requests
from config import SLACK_TOKEN

filename = 'pitpremium_bdowdy_bonus.mp3'
files = {'file': "open(f'posts/{filename}', 'rb')"}
payload = {
    'token': '6MOCdnY9JgumIMESR3hSiWKG',
    'channels': ['#random'],
}
url = 'https://slack.com/api/auth.test'

# r = requests.post(url, params=payload, files=files) 
r = requests.post(url, data=payload)
print(r.text)
