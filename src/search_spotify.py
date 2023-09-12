import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
import model.spotify_search as Spotify

from src.get_token import update_token, return_token

import requests

def deduplicate(models) :
    ids_uniq = set(model.id for model in models)
    uniq = list()
    for model in models :
        if model.id in ids_uniq :
            uniq.append(model)
            ids_uniq.remove(model.id)
    return uniq

def deduplicate_by_filter(models,models_filter) :
    ids_uniq = set(model.id for model in models_filter)
    uniq = list()
    for model in models :
        if model.id in ids_uniq :
            uniq.append(model)
            ids_uniq.remove(model.id)
    return uniq

def search_spotify(input:str) :
    access_token = return_token()
    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q={keyword}'.format(keyword=input)
                            +'&type=artist%2Calbum%2Ctrack'
                            +'&limit=50'
                            +'&offset=0'
                      ,headers={
                          'Authorization': 'Bearer '+ access_token
                      }
                      )
    
    if response.status_code == 200 :
        responsed_data = response.json()
        parsed_data = Spotify.Search(**responsed_data)

        tracks_data = parsed_data.tracks.items
        albums_data = [track.album for track in tracks_data]
        artists_filter = [artist for track in tracks_data for artist in track.artists]
        artists_data = parsed_data.artists.items

        search_result = dict(
            tracks = deduplicate(tracks_data)
            , albums = deduplicate(albums_data)
            , artists = deduplicate_by_filter(artists_data,artists_filter)
        )

        return search_result

def load_spotify(search_result) :
    tracks = [Spotify.TracksORM(track) for track in search_result.get('tracks')]
    albums = [Spotify.AlbumsORM(album) for album in search_result.get('albums')]
    artists = [Spotify.ArtistsORM(artist) for artist in search_result.get('artists')]

    with session_scope() as session :
        session.add_all(tracks)
        session.add_all(albums)
        session.add_all(artists)

def convert_timestamp(timestamp:str) :
    minutes = timestamp // 60
    seconds = timestamp % 60
    return f'{minutes}:{seconds}'

def format_search(data:Spotify.Search) :
    search_output = dict()
    # search_output['tracks'] = [{'name':track.name, 'img':None, 'artist':None, 'duration':None} for track in tracks]
    # search_output['albums'] = [{'name':album.name, 'img':album.images_url, 'artist':None, 'release_year':None} for album in albums]
    # search_output['artists'] = [{'name':artist.name, 'img':None} for artist in artists]

    return search_output

if __name__ == '__main__':
    # update_token('iamsophie')
    access_token = return_token()

    search_result = search_spotify('아이유')
    load_spotify(search_result)
    # search_output = format_search(search_result)
    # print(search_output)