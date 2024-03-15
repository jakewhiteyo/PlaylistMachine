from controllers.spotify_controller import SpotifyAPI
from controllers.reddit_controller import RedditAPI
from controllers.openai_controller import OpenAiAPI
from utils.helpers import cleanse_string
import json

class PlaylistMachine:
  def __init__(self):
    self.spotify_api = SpotifyAPI()
    self.reddit_api = RedditAPI()
    self.openai_api = OpenAiAPI()

  def MikeDean(self):   
    # 1. query reddit for edm announcements 
    posts = self.GetMusicPosts()
    if(len(posts) < 1): return
    
    json_str = json.dumps(posts, indent=4)
    print(json_str)
    
    # 2. generate prompt
    prompt = self.CreatePlaylistPrompt(posts)
    print(prompt)
    
    # 3. ask chat GPT for SEO playlist names for each relevant title/description
    playlist_names = self.QueryForPlaylistNames(prompt)
    print(playlist_names)

    # 4. Get songs for each playlist

    # 5. Create Spotify Playlist

    # 6. Add songs to Spotify Playlist
    
    

  def GetMusicPosts(self):
    subreddit = 'edm'
    flairs = ['upcoming'] # can add 'music' flair if we're feeling crazy
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
  

  def CreatePlaylistPrompt(self, posts):
    prompt = f"Here are {len(posts)} Reddit post titles. For each of the posts that could be translated into a playlist, return with an SEO optimized playlist name. Here are the post titles: "
    titles = [post["title"] for post in posts]
    prompt += "\n-"
    prompt += "\n- ".join(titles)
    return prompt

  def QueryForPlaylistNames(self, prompt):
    response = self.openai_api.query_chat(prompt)
    playlist_names = cleanse_string(response)
    return playlist_names
