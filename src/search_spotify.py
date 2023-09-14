import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
import model.spotify_search as Spotify

import requests
import json

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

def search_spotify(keywords:str,limit:int=3,offset:int=0) :
    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q={q}'.format(q=keywords)
                            +'&type=artist%2Calbum%2Ctrack'
                            +'&limit={limit}'.format(limit=limit)
                            +'&offset={offset}'.format(offset=offset)
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

        search_result = Spotify.SearchResult(
            tracks = deduplicate(tracks_data)
            , albums = deduplicate(albums_data)
            , artists = deduplicate_by_filter(artists_data,artists_filter)
        )
        return search_result

def convert_timestamp(millis:int) :
    seconds = millis // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    duration = [hours, f'{minutes:02}', f'{seconds:02}'][hours == 0 :]
    return ':'.join(map(str, duration))
    
def format_search(search_result:Spotify.SearchResult) :
    tracks = search_result.tracks
    albums = search_result.albums
    artists = search_result.artists

    tracks_output = [dict(
                        name=track.name
                        ,img=track.album.images[0].url
                        ,artists=', '.join([artist.name for artist in track.artists])
                        ,duration=convert_timestamp(int(track.duration_ms))
                    ) for track in tracks]
    albums_output = [dict(
                        name=album.name
                        ,img=album.images[0].url
                        ,artists=', '.join([artist.name for artist in album.artists])
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
    print(f'################### 검색결과 ################### \n'
          + f'# tracks:{len(tracks_output)}\n'
          + f'# albums:{len(tracks_output)}\n'
          + f'# artists:{len(tracks_output)}\n')
    print(json.dumps(search_output,indent=2))

    return search_output

def load_spotify(search_result:Spotify.SearchResult) :
    tracks = [Spotify.TracksORM(track) for track in search_result.tracks]
    albums = [Spotify.AlbumsORM(album) for album in search_result.albums]
    artists = [Spotify.ArtistsORM(artist) for artist in search_result.artists]

    with session_scope() as session :
        session.add_all(tracks)
        session.add_all(albums)
        session.add_all(artists)

if __name__ == '__main__':

    # 0 - get spotify token
    from src.get_token import update_token, return_token
    # update_token('iamsophie')
    access_token = return_token()

    # 1 - spotify api search
    search_result = search_spotify('아이유')
    
    # 2 - for search result page
    search_output = format_search(search_result)

    # # 3 - load db : spotify_tracks, spotify_albums, spotify_artists
    # load_spotify(search_result)

    # # 4 - load db : lyrics_temp
    # from src.lyric import lyric_search_and_input, GENIUS_API_KEY
    # for track in search_result.tracks :
    #     lyric_search_and_input(
    #         track_id=track.id
    #         ,track=track.name
    #         ,artist=', '.join([artist.name for artist in track.artists])
    #         ,GENIUS_API_KEY=GENIUS_API_KEY
    #     )
    
    # # 5 - load db : spotify_audio_features
    # from src.get_audio_features import load_audio_features
    # for track in search_result.tracks :
    #     load_audio_features(
    #         id=track.id
    #     )