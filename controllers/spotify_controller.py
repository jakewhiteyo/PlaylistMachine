import json
import requests
from requests.auth import HTTPBasicAuth
import os
import urllib.parse

class SpotifyAPI:
    
    def __init__(self):
        self.client_id = os.environ.get('SPOTIFY_CLIENT_ID', '')
        self.client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET', '')
        self.refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN', '')
        self.user_id = os.environ.get('SPOTIFY_USER_ID')
        self.refresh_access_token()

    def refresh_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        payload = {
            'grant_type': 'refresh_token',  
            'refresh_token': self.refresh_token
        }

        response = requests.post(url, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=payload)

        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return response.json()
        else:
            return {'error': 'Failed to refresh token', 'details': response.json()}, response.status_code

    # search for spotify artists related to query
    def get_artists(self, query, limit=10):
        if not self.access_token:
            return {'error' : 'Access token undefined'} 
        
        url = f"https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "q": urllib.parse.quote(query),
            "type": "artist",
            "limit": limit
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    # search for spotify playlists related to query
    def get_playlists(self, query, limit=3):
        if not self.access_token:
            return {'error': 'Access token undefined'}

        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        params = {
            "q": query,
            "type": "playlist",
            "limit": limit
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    # Search for an artist by name and return their Spotify ID.
    def get_artist_id(self, artist_name):
        search_url = 'https://api.spotify.com/v1/search'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}
        response = requests.get(search_url, headers=headers, params=params)
        results = response.json()
        return results['artists']['items'][0]['id']

    def get_artist_songs(self, artist_id):
        albums_url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'include_groups': 'album,single', 'limit': 50}
        response = requests.get(albums_url, headers=headers, params=params)
        albums = response.json()['items']
        
        tracks = []
        for album in albums:
            album_id = album['id']
            tracks_url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
            tracks_response = requests.get(tracks_url, headers=headers)
            tracks_data = tracks_response.json()['items']
            for track in tracks_data:
                tracks.append(track['name'])
        
        return tracks

    # search spotify for song
    def get_song(self, query, limit=1):
        if not self.access_token:
            return {'error': 'Access token undefined'}

        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        params = {
            "q": query,
            "type": "track",
            "limit": limit
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    # get the songs on a playlist
    def get_playlist_tracks(self, playlist_id, limit=50, offset=0):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        params = {
            "limit": limit,  # The maximum number of items to return (1..100)
            "offset": offset  # The index of the first item to return
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def create_playlist(self, playlist_name, playlist_description):
        print(f"creating playlist {playlist_name}")
        
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        # Headers and payload for the POST request
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": playlist_name,
            "description": playlist_description,
            "public": True  # Set to True if you want the playlist to be public
        }

        # Make the POST request to create the new playlist
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))

        return response.json()


    def add_playlist_tracks(self, playlist_id, uris):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        # Headers and payload for the POST request
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = json.dumps({
            "uris": uris
        })


        # Make the POST request to add songs to the playlist
        response = requests.post(url, headers=headers, data=data)

        return response.json()
