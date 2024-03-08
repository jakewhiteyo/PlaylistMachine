from controllers.spotify_controller import SpotifyAPI
from controllers.reddit_controller import RedditAPI
from controllers.openai_controller import OpenAiAPI
import json

class PlaylistMachine:
  def __init__(self):
    self.spotify_api = SpotifyAPI()
    self.reddit_api = RedditAPI()
    self.openai_api = OpenAiAPI()

  def MikeDean(self):   
    # 1. query reddit for edm announcements 
    posts = self.GetMusicPosts()
    json_str = json.dumps(posts, indent=4)
    print(json_str)
    # 2. generate prompt
    
    # 3. ask chat GPT for SEO playlist names for each relevant title/description
    self.GetPlaylistNames()
    pass
    

  def GetMusicPosts(self):
    subreddit = 'edm'
    flairs = ['upcoming', 'music']
    posts = self.reddit_api.fetch_posts(subreddit)
    announcements = []
    for post in posts:
      post_data = post['data']
      flair = post_data.get('link_flair_text', 'No Flair')
      if(flair.lower() in flairs):
        title = post_data.get('title', 'No Title')
        description = post_data.get('selftext', 'No Description')
        upvotes = post['data']['ups']
        announcements.append({
          "title":title,
          "description":description,
          "upvotes":upvotes,
          "flair":flair
        })
    return announcements
  
  def GetPlaylistNames(self):
    response = self.openai_api.query_chat("Hows it going")
