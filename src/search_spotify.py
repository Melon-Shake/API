from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from model.database import session_scope
import model.spotify_search as Spotify

import requests
from urllib.parse import urlparse, parse_qs
from fastapi.encoders import jsonable_encoder
import model.spotify_search as Spotify
import model.metadata as Meta
import model.database as db
from src.get_token import update_token, return_token


# 0 - get token and set header

access_token = update_token('iamsophie')
access_token = return_token()
search_header = {'Authorization': f'Bearer {access_token}'}


# 1 - spotify API responsed_data -> parsed_data

def search_by_keywords(keywords:str,type:list[str]=['artist','album','track'],limit:int=3,offset:int=0) :
    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q={}'.format(keywords)
                            +'&type={}'.format('%2C'.join(type))
                            +'&limit={}'.format(limit)
                            +'&offset={}'.format(offset)
                            ,headers=search_header)

    response_code = response.status_code
    if response_code == 200 :
        responsed_data = response.json()

        try : parsed_data = Spotify.Search(**responsed_data)
        except :
            parsed_data = Spotify.Search(
                artists=(Spotify.SearchArtists(**responsed_data.get('artists')) if 'artists' in responsed_data else None),
                albums=(Spotify.SearchAlbums(**responsed_data.get('albums')) if 'albums' in responsed_data else None),
                tracks=(Spotify.SearchTracks(**responsed_data.get('tracks')) if 'tracks' in responsed_data else None)
            )
        return parsed_data
    
    elif response_code == 401 :
        print(f'search_by_keywords() - 토큰만료오류')
    elif response_code == 404 :
        print(f'search_by_keywords() - 리퀘스트오류')
    else : print(f'search_by_keywords() - {response.status_code}')

def search_by_query(query_params:dict[str,list]) :
    keywords = query_params.get('q' or 'query').pop()
    type = query_params.get('type').pop().split(',')
    limit = query_params.get('limit').pop()
    offset = query_params.get('offset').pop()

    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q={}'.format(keywords)
                            +'&type={}'.format('%2C'.join(type))
                            +'&limit={}'.format(limit)
                            +'&offset={}'.format(offset)
                            ,headers=search_header)

    response_code = response.status_code
    if response_code == 200 :
        responsed_data = response.json()

        try : parsed_data = Spotify.Search(**responsed_data)
        except :
            parsed_data = Spotify.Search(
                artists=(Spotify.SearchArtists(**responsed_data.get('artists')) if 'artists' in responsed_data else None),
                albums=(Spotify.SearchAlbums(**responsed_data.get('albums')) if 'albums' in responsed_data else None),
                tracks=(Spotify.SearchTracks(**responsed_data.get('tracks')) if 'tracks' in responsed_data else None)
            )
        return parsed_data

    elif response_code == 401 :
        print(f'search_by_keywords() - 토큰만료오류')
    elif response_code == 404 :
        print(f'search_by_keywords() - 리퀘스트오류')
    else : print(f'search_by_keywords() - {response.status_code}')

def search_by_id(type:str,id:str) :
    type = type[:-1]
    response = requests.get(f'https://api.spotify.com/v1/{type}s/{id}'
                            ,headers=search_header)

    response_code = response.status_code
    if response_code == 200 :
        responsed_data = response.json()

        parsed_data = None
        if type == 'artist' :
            parsed_data = Spotify.ArtistsExt(**responsed_data)
        elif type == 'album' :
            parsed_data = Spotify.AlbumsExt(**responsed_data)
        elif type == 'track' :
            parsed_data = Spotify.TracksExt(**responsed_data)
        return parsed_data
    
    elif response_code == 401 :
        print(f'search_by_keywords() - 토큰만료오류')
    elif response_code == 404 :
        print(f'search_by_keywords() - 리퀘스트오류')
    else : print(f'search_by_keywords() - {response.status_code}')

def search_by_href(href:str) :
    parsed_url = urlparse(href)
    if not parsed_url.query :
        path_params = parsed_url.path.split('/')
        type = path_params[-2]
        id = path_params[-1]
        return search_by_id(type,id)
    else : 
        query_params = parse_qs(parsed_url.query)
        return search_by_query(query_params=query_params)


# 2 - parsed_data -> culled_data

def deduplicate(models:list[object]) :
    ids_uniq = set(model.id for model in models)
    uniq = list()
    for model in models :
        if model.id in ids_uniq :
            uniq.append(model)
            ids_uniq.remove(model.id)
    return uniq

def deduplicate_by_filter(models:list[object],models_filter:list[object]) :
    ids_uniq = set(model.id for model in models_filter)
    uniq = list()
    for model in models :
        if model.id in ids_uniq :
            uniq.append(model)
            ids_uniq.remove(model.id)
    return uniq

def cull_data(parsed_data:Spotify.Search) :
    tracks_data = parsed_data.tracks.items

    albums_data = [track.album for track in tracks_data]
    albums_data = deduplicate(albums_data)

    artists_data = [artist for track in tracks_data for artist in track.artists]
    artists_data = deduplicate(artists_data)
    artists_data = [search_by_href(artist.href) for artist in artists_data]

    culled_data = Spotify.SearchResult(
        tracks=tracks_data,
        albums=albums_data,
        artists=artists_data
    )
    return culled_data


# 3 - culled_data -> search_data

def convert_timestamp(millis:int) :
    seconds = millis // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    duration = [hours, f'{minutes:02}', f'{seconds:02}'][hours == 0 :]
    return ':'.join(map(str, duration))

def return_search(search_result:Spotify.SearchResult) :
    tracks = search_result.tracks
    albums = search_result.albums
    artists = search_result.artists

    tracks_result = [Meta.Track(
                        name=track.name
                        ,img=track.album.images[0].url if hasattr(track.album,'images') and not track.album.images else None
                        ,artists=', '.join([artist.name for artist in track.artists])
                        ,duration=convert_timestamp(int(track.duration_ms))
                    ) for track in tracks]
    albums_result = [Meta.Album(
                        name=album.name
                        ,img=album.images[0].url if hasattr(album,'images') and not album.images else None
                        ,artists=', '.join([artist.name for artist in album.artists])
                        ,release_year=album.release_date
                    ) for album in albums]
    artists_result = [Meta.Artist(
                        name=artist.name
                        ,img=artist.images[0].url if hasattr(artists,'images') and not artist.images else None
                    ) for artist in artists]
    
    search_result = Meta.SearchResult(
        artists=artists_result,
        albums=albums_result,
        tracks=tracks_result
    )
    return search_result

# 3 - culled_data -> load db : spotify_artists, spotify_albums, spotify_tracks

def load_spotify(search_result:Spotify.SearchResult) :
    tracks = [Spotify.TracksORM(track) for track in search_result.tracks]
    albums = [Spotify.AlbumsORM(album) for album in search_result.albums]
    artists = [Spotify.ArtistsORM(artist) for artist in search_result.artists]

    with db.session_scope() as session :
        session.add_all(tracks)
        session.add_all(albums)
        session.add_all(artists)


# 4 - load and update db : spotify_audio_featurs, lyrics, audio_features

def get_audio_features(track_id:str) :
    response = requests.get(f'https://api.spotify.com/v1/audio-features/{track_id}'
                            ,headers=search_header)
    
    response_code = response.status_code
    if response_code == 200 :
        responsed_data = response.json()

        parsed_data = Spotify.AudioFeatures(**responsed_data)
        return parsed_data

    elif response_code == 401 :
        print(f'search_by_keywords() - 토큰만료오류')
    elif response_code == 404 :
        print(f'search_by_keywords() - 리퀘스트오류')
    else : print(f'search_by_keywords() - {response.status_code}')

def bring_lucete(tracks_data:list[Spotify.TracksExt]) :
    from src.lyric import lyric_search_and_input, GENIUS_API_KEY
    from src.lyrics_analyze import lyrics_analyze
    from src.track_analyze import audio_features_update

    audios = list()
    for track in tracks_data :
        audios.append(Spotify.AudioFeaturesORM(get_audio_features(track.id)))
    with db.session_scope() as session :
        session.add_all(audios)
