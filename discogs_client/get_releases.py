import requests
from config import TOKEN, USER_AGENT


token = 'SnlTMGMAzKlTXhTKfZvBrfzTtrQvEIykxMrzSZQr'
headers = {'user-agent': USER_AGENT}
params = {'q': 'kyuss', 'type': 'artist', 'token': token}
resp = requests.get('https://api.discogs.com/database/search', headers=headers, params=params)
res = resp.json()
artist_resource = res['results'][0]['resource_url']
release_resource  = artist_resource + '/releases'
releases = requests.get(release_resource, headers=headers, params={'token': token}).json()

