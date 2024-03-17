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
      # { 'playlist_name': '2005 by Childish Gambino', 'reddit_post_title': 'New album 2005 by Childish Gambino dropping soon','artists': ['Childish Gambino']}
    playlist_names = self.QueryForPlaylistNames(prompt)
    print("\n___ Playlist Names ___")
    print(playlist_names)
    print("\n")

    #playlist_names = [
    #  {
    #    'playlist_name': 'Stayinit - Fred Again, Overmono, Lil Yachty',
    #     'reddit_post_title': 'New song by Fred Again, Overmono, and Lil Yachty - Stayinit',
    #     'artists': ['Fred Again', 'Overmono', 'Lil Yachty']
    #  }
    #]

    # 4. Get songs for each playlist / Create Spotify Playlist
    playlists = []
    for playlist_data in playlist_names:
      playlist_name = playlist_data.get('playlist_name')
      if(playlist_name is None): continue
      
      reference_songs = self.GetPlaylistSongs(playlist_name)

      playlists.append({
        'name': playlist_name,
        'songs': reference_songs
      })
    
    print("\n_____Playlists_____")
    print(json.dumps(playlists, indent=4))

    # 5. Create Spotify Playlists and add songs
    for playlist in playlists:
      playlist_name = playlist.get('name')
      playlist_songs = playlist.get('songs')
      # Create Spotify Playlist
      create_playlist_response = self.spotify_api.create_playlist(playlist_name, "test description")
      new_playlist_id = create_playlist_response.get('id')

      # Add songs to playlist
      playlist_songs = [song['uri'] for song in playlist_songs]
      self.spotify_api.add_playlist_tracks(new_playlist_id, playlist_songs)

    
  
  def GetPlaylistSongs(self, playlist_name):
    songs = []
    # find 3 spotify playlists with a similar name
    spotify_playlists = self.spotify_api.get_playlists(playlist_name).get('playlists').get('items')
    # get first 10 songs in each playlist
    for playlist in spotify_playlists:
      playlist_id = playlist.get('id')
      playlist_songs = self.spotify_api.get_playlist_tracks(playlist_id, 10).get('items')
      for song in playlist_songs:
        songs.append({
          'name': song.get('track').get('name'),
          'artist': song.get('track').get('artists')[0].get('name'),
          'uri': song.get('track').get('uri')
        })
    return songs

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
    prompt = "Here are some Reddit posts. For each of the posts that could be translated into a SEO optimized spotify playlist - because it describes an upcoming song, album, or concert - create a playlist title and add it to a list of JSON objects in this format: \n{ 'playlist_name': '2005 - Childish Gambino', 'reddit_post_title': 'New album 2005 by Childish Gambino dropping soon','artists': ['Childish Gambino']}\n Respond with the JSON object and nothing else. Here are the reddit posts:\n"
    json_str = json.dumps(posts, indent = 3)
    prompt += json_str

    return prompt

  def QueryForPlaylistNames(self, prompt):
    names = self.openai_api.query_chat(prompt)
    print(names)
    return json.loads(names)
