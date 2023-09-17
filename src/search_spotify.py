from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

import requests
from urllib.parse import urlparse, parse_qs
from fastapi.encoders import jsonable_encoder
import model.spotify_search as Spotify

import requests
from urllib.parse import urlparse, parse_qs
from fastapi.encoders import jsonable_encoder

import model.database as DB
import model.metadata as Meta
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

def deduplicate_by_filter(models:list[object],models_filter:list[object]) :
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

def return_search(search_result:Spotify.SearchResult) :
    tracks = search_result.tracks
    albums = search_result.albums
    artists = search_result.artists

    tracks_result = [Meta.Track(
    tracks_result = [Meta.Track(
                        name=track.name
                        ,img=track.album.images[0].url if hasattr(track.album,'images') and track.album.images and track.album.images[0].url else None
                        ,artists=', '.join([artist.name for artist in track.artists])
                        ,duration=convert_timestamp(int(track.duration_ms))
                    ) for track in tracks]
    albums_result = [Meta.Album(
    albums_result = [Meta.Album(
                        name=album.name
                        ,img=album.images[0].url if hasattr(album,'images') and album.images and album.images[0].url else None
                        ,artists=', '.join([artist.name for artist in album.artists])
                        ,release_year=album.release_date
                    ) for album in albums]
    artists_result = [Meta.Artist(
    artists_result = [Meta.Artist(
                        name=artist.name
                        ,img=artist.images[0].url if hasattr(artist,'images') and artist.images and artist.images[0].url else None
                    ) for artist in artists]
    
    search_result = Meta.SearchResult(
        artists=artists_result,
        albums=albums_result,
        tracks=tracks_result
    
    search_result = Meta.SearchResult(
        artists=artists_result,
        albums=albums_result,
        tracks=tracks_result
    )
    return search_result

# 3 - culled_data -> load db : spotify_artists, spotify_albums, spotify_tracks

def load_spotify(search_result:Spotify.SearchResult) :
    tracks = list()
    audios = list()
    for track in search_result.tracks :
        tracks.append(Spotify.TracksORM(track))
        audios.append(Spotify.AudioFeaturesORM(get_audio_features(track.id)))
    albums = [Spotify.AlbumsORM(album) for album in search_result.albums]
    artists = [Spotify.ArtistsORM(artist) for artist in search_result.artists]

    with DB.session_scope() as session :
        session.add_all(tracks)
        session.add_all(audios)
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
        print(f'get_audio_features() - 토큰만료오류')
    elif response_code == 404 :
        print(f'get_audio_features() - 리퀘스트오류')
    else : print(f'get_audio_features() - {response.status_code}')