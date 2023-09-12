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
    
def deduplicate(models) :
    ids_uniq = set(model.id for model in models)
    uniq = list()
    for model in models :
        if model.id in ids_uniq :
            uniq.append(model)
            ids_uniq.remove(model.id)
    return uniq

def load_spotify(data:Spotify.Search) :
    tracks = data.tracks.items
    albums = [track.album for track in tracks]
    artists = [artist for track in tracks for artist in track.artists]

    tracks_orm = [Spotify.TracksORM(track) for track in deduplicate(tracks)]
    albums_orm = [Spotify.AlbumsORM(album) for album in deduplicate(albums)]
    artists_orm = [Spotify.ArtistsORM(artist) for artist in deduplicate(artists)]

    with session_scope() as session :
        session.add_all(tracks_orm)
        session.add_all(albums_orm)
        session.add_all(artists_orm)

def convert_timestamp(timestamp:str) :
    minutes = timestamp // 60
    seconds = timestamp % 60
    return f'{minutes}:{seconds}'

def format_search(data:Spotify.Search) :
    search_output = dict()
    # search_output['tracks'] = [{'name':track.name, 'img':None, 'artist':None, 'duration':None} for track in tracks]
    # search_output['albums'] = [{'name':album.name, 'img':album.images_url, 'artist':None, 'release_year':None} for album in albums]
    # search_output['artists'] = [{'name':artist.name, 'img':None} for artist in artists]

    # for track in data.tracks.items :
        
    #     track.name
    #     track.album.images[0].url
    #     ', '.join([artist.name for artist in track.artists])
    #     convert_timestamp(track.duration_ms)

    #     track.album.name
    #     track.album.images[0].url
    #     ', '.join([artist.name for artist in track.album.artists])

    return search_output

if __name__ == '__main__':
    update_token('iamsophie')
    access_token = return_token()

    search_result = search_spotify('아이유')
    load_spotify(search_result)
    # search_output = format_search(search_result)
    # print(search_output)