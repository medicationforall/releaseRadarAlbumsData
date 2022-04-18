import sys
sys.path.append(".")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import config

scope = "playlist-read-private"

def collect_new_release_tracks():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=config.client_id, client_secret=config.client_secret, redirect_uri=config.redirect_uri))
    release_radar_tracks = sp.playlist_items(config.playlist_id, limit=100)
    release_radar_tracks2 = sp.playlist_items(config.playlist_id, limit=100, offset=100)
    items = release_radar_tracks['items'] + release_radar_tracks2['items']

    singles = []
    albums = []

    for item in items:
        album_type = item['track']['album']['album_type']
        if album_type=='single':
            singles.append(item)
        else:
            albums.append(item)

    print('singles', len(singles))
    print('albums', len(albums))
    __process_albums(albums)

def __process_albums(albums):
    albums_data = []
    for album in albums:
        album_data = {}
        album_data['name'] = album['track']['album']['name']
        album_data['tracks'] = album['track']['album']['total_tracks']
        album_data['artists'] = []
        album_data['artist_urls'] = []
        album_data['release_date'] = album['track']['album']['release_date']
        album_data['url'] = album['track']['album']['external_urls']['spotify']
        album_data['image'] = album['track']['album']['images'][-1]['url']

        for artist in album['track']['album']['artists']:
            artist_name = artist['name']
            spotify_url = artist['external_urls']['spotify']
            album_data['artist_urls'].append(spotify_url)
            album_data['artists'].append(artist_name)

        if len(album_data['artists'])  == 1:
            album_data['artists'] = album_data['artists'][0]
            album_data['artist_urls'] = album_data['artist_urls'][0]
        albums_data.append(album_data)

    json_albums = json.dumps(albums_data)

    with open('./out/albums.json', 'w') as outfile:
        outfile.write(json_albums)

if __name__ == "__main__":
    print('this is the main runner')
    collect_new_release_tracks()
