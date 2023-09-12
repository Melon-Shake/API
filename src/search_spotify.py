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
                            +'&limit=3'
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

def convert_timestamp(millis) :
    seconds = millis // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    duration = [hours, f'{minutes:02}', f'{seconds:02}'][hours == 0 :]
    return ':'.join(map(str, duration))
    
def format_search(search_result) :
    tracks = search_result.get('tracks')
    albums = search_result.get('albums')
    artists = search_result.get('artists')

    tracks_output = [dict(
                        name=track.name
                        ,img=track.album.images[0].url
                        ,artist=', '.join([artist.name for artist in track.artists])
                        ,duration=convert_timestamp(int(track.duration_ms))
                    ) for track in tracks]

    albums_output = [dict(
                        name=album.name
                        ,img=album.images[0].url
                        ,artist=', '.join([artist.name for artist in album.artists])
                        ,release_year=album.release_date
                    ) for album in albums]
    artists_output = [dict(
                        name=artist.name
                        ,img=artist.images[0].url
                    ) for artist in artists]

    search_output = dict(
        tracks=tracks_output
        ,albums=albums_output
        ,artists=artists_output
    )
    return search_output

if __name__ == '__main__':
    update_token('iamsophie')
    access_token = return_token()

    search_result = search_spotify('아이유')
    load_spotify(search_result)
    search_output = format_search(search_result)
    import json
    print(json.dumps(search_output,indent=2))