from flask_restx import Namespace, Resource
from controllers.spotify_controller import SpotifyAPI
from controllers.reddit_controller import RedditAPI
from flask import request
from utils.playlist_machine import PlaylistMachine

api_namespace = Namespace("Routes", description="Playlist Machine Routes")
spotify_api = SpotifyAPI()
reddit_api = RedditAPI()

playlist_machine = PlaylistMachine()

@api_namespace.route("/edm")
class ScrapeEDM(Resource):
    def get(self):
        playlist_machine.MikeDean()
 
@api_namespace.route("/internal/refresh-token") 
class RefreshToken(Resource): 
  def post(self): 
    return spotify_api.refresh_access_token() 
   
@api_namespace.route("/get-artists") 
@api_namespace.param('query', 'The search query for the artist', _in='query')
class GetArtists(Resource):
    def get(self):
        search_query = request.args.get('query')
        
        # Ensure that a search query was provided
        if not search_query:
            return {"error": "No search query provided"}, 400
        
        # Call Spotify API client method to search for artists
        return spotify_api.get_artists(search_query)

@api_namespace.route("/get-playlists")
@api_namespace.param('query', 'The search query for the playlist', _in='query')
class GetPlaylists(Resource):
    def get(self):
        search_query = request.args.get('query')
        
        # Ensure that a search query was provided
        if not search_query:
            return {"error": "No search query provided"}, 400
        
        # Call Spotify API client method to search for artists
        return spotify_api.get_playlists(search_query)


@api_namespace.route("/get-song")
@api_namespace.param('query', 'The search query for a song', _in='query')
class GetSong(Resource):
    def get(self):
        search_query = request.args.get('query')
        
        # Ensure that a search query was provided
        if not search_query:
            return {"error": "No search query provided"}, 400
        
        # Call Spotify API client method to search for artists
        return spotify_api.get_song(search_query)
    

@api_namespace.route("/internal/get-playlist-songs")
@api_namespace.param('playlist-id', 'Playlist ID', _in='query')
class GetPlaylistSongs(Resource):
    def get(self):
        playlist_id = request.args.get('playlist-id')
        
        # Ensure that a search query was provided
        if not playlist_id:
            return {"error": "No search query provided"}, 400
        
        # Call Spotify API client method to search for artists
        return spotify_api.get_playlist_tracks(playlist_id)

@api_namespace.route("/generate")
@api_namespace.param('keywords', 'playlist/genre keywords', _in='query')
@api_namespace.param('artist-names', 'names of artists', _in='query')
@api_namespace.param('song-names', 'names of songs', _in='query')
@api_namespace.param('playlist-ids', 'Playlist IDs', _in='query')
class Generate(Resource):
    def get(self):
        keywords = request.args.get('keywords').split(',')
        artist_names = request.args.get('artist-names').split(',')
        song_names = request.args.get('song-names').split(',')
        playlist_ids = request.args.get('playlist-ids').split(',')

        print(keywords)
        print(song_names)
        print(artist_names)
        print(playlist_ids)
        
        # Ensure that a search query was provided
        # if not playlist_id:
        #     return {"error": "No search query provided"}, 400
        
        # Call Spotify API client method to search for artists
        #return spotify_api.get_playlist_tracks(playlist_id)
