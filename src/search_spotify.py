import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
import model.spotify_search as Spotify

from src.get_token import update_token, return_token

import requests

def search_spotify(input:str) :
    access_token = return_token()
    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q={keyword}'.format(keyword=input)
                            +'&type=artist%2Calbum%2Ctrack'
                            +'&limit=50'
                            # +'&offset=3'
                      ,headers={
                          'Authorization': 'Bearer '+ access_token
                      }
                      )
    
    if response.status_code == 200 :
        responsed_data = response.json()
        parsed_data = Spotify.Search(**responsed_data)
        return parsed_data

def load_spotify(data:Spotify.Search) :
    unique_tracks = set(str(track) for track in data.tracks.items)
    unique_albums = set(str(track.album) for track in data.tracks.items)
    unique_artists = set(str(artist) for track in data.tracks.items for artist in track.artists)

    tracks = [Spotify.TracksORM(track) for track in unique_tracks]
    albums = [Spotify.AlbumsORM(album) for album in unique_albums]
    artists = [Spotify.ArtistsORM(artist) for artist in unique_artists]

    with session_scope() as session :
        session.add_all(tracks)
        session.add_all(albums)
        session.add_all(artists)

def format_search(data:Spotify.Search) :
    tracks = [Spotify.TracksORM(track) for track in data.tracks.items]
    albums = [Spotify.AlbumsORM(track.album) for track in data.tracks.items]
    artists = [Spotify.ArtistsORM(artist) for track in data.tracks.items for artist in track.artists]

    search_output = dict()
    search_output['tracks'] = [{'name':track.name, 'img':None, 'artist':None, 'duration':None} for track in tracks]
    search_output['albums'] = [{'name':album.name, 'img':album.images_url, 'artist':None, 'release_year':None} for album in albums]
    search_output['artists'] = [{'name':artist.name, 'img':None} for artist in artists]

    return search_output

if __name__ == '__main__':
    # update_token('iamsophie')
    access_token = return_token()

    search_result = search_spotify('아이유')
    # load_spotify(search_result)
    search_output = format_search(search_result)
    print(search_output.get('tracks')[0])