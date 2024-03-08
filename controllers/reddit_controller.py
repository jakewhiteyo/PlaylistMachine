import requests
from requests.auth import HTTPBasicAuth
import os

class RedditAPI:

  def __init__(self):
    self.client_id = os.environ.get('REDDIT_CLIENT_ID', '')
    self.client_secret = os.environ.get('REDDIT_CLIENT_SECRET', '')
    self.user_agent = "Playlist Machine by Jake White"

  def get_access_token(self):
    auth = HTTPBasicAuth(self.client_id, self.client_secret)
    data = {'grant_type': 'client_credentials'}
    headers = {'User-Agent': self.user_agent}
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers).json()
    print("response", response)
    # token_info = {
    #     'access_token': response['access_token'],
    #     'expires_at': time.time() + response['expires_in']
    # } 
    return response['access_token']


  def fetch_posts(self, subreddit):
    access_token = self.get_access_token()
    print("fetching posts")
    headers = {
        'Authorization': f'bearer {access_token}',
        'User-Agent': self.user_agent
    }
    response = requests.get(f'https://oauth.reddit.com/r/{subreddit}/new', headers=headers, params={'limit': 100})
    if response.status_code == 200:
        posts = response.json()['data']['children']
        return posts
    else:
        print(f'Failed to fetch posts. Status code: {response.status_code}')
