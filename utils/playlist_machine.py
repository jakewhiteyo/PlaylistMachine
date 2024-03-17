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
    edm_posts = self.GetMusicPosts('edm', ['upcoming'])
    electronic_posts = self.GetMusicPosts('electronicmusic', ['news'])
    posts = edm_posts + electronic_posts
    
    print("\n___ POSTS ___")
    json_str = json.dumps(posts, indent=4)
    print(json_str)
    print("\n")

    if(len(posts) < 1): 
      print("no posts")
      return
    
    
    # 2. generate prompt
    prompt = self.CreatePlaylistPrompt(posts)
    print("\n___ PROMPT ___")
    print(prompt)
    print("\n")
    
    # 3. ask chat GPT for SEO playlist names for each relevant title/description
    playlist_names = self.QueryForPlaylistNames(prompt)
    print("\n___ Playlist Names ___")
    print(playlist_names)
    print("\n")

    # 4. Get songs for each playlist

    # 5. Create Spotify Playlist

    # 6. Add songs to Spotify Playlist
    
    

  def GetMusicPosts(self, subreddit, flairs):
    posts = self.reddit_api.fetch_posts(subreddit)
    announcements = []
    for post in posts:
      post_data = post['data']
      flair = post_data.get('link_flair_text')
      if(flair != None and flair.lower() in flairs):
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
    prompt = "Here are some Reddit posts. For each of the posts that could be translated into a SEO optimized spotify playlist - because it describes an upcoming song, album, or concert - create a playlist title and add it to a list of JSON objects in this format: \n{ 'playlist_name': '2005 by Childish Gambino', 'reddit_post_title': 'New album 2005 by Childish Gambino dropping soon','artists': ['Childish Gambino']}\n Respond with the JSON object and nothing else. Here are the reddit posts:\n"
    json_str = json.dumps(posts, indent = 3)
    prompt += json_str

    return prompt

  def QueryForPlaylistNames(self, prompt):
    names = self.openai_api.query_chat(prompt)
    print(names)
    return json.loads(names)
