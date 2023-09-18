from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

import model.database as DB
import model.spotify_search as Spotify

import requests
from urllib.parse import urlparse, parse_qs
from fastapi.encoders import jsonable_encoder

import model.database as DB
import model.metadata as Meta
import model.spotify_search as Spotify
from src.get_token import update_token, return_token


# 0 - get token and set header

access_token = update_token('iamsophie')
access_token = return_token()
search_header = {'Authorization': f'Bearer {access_token}'}


# 1 - spotify API responsed_data -> parsed_data

def get_artist_albums(artist_id:str, limit:int=50,offset:int=0) :
    response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/albums'
                            +'?limit={}&offset={}'.format(limit,offset)
                            ,headers=search_header)
    response_code = response.status_code
    if response_code == 200 :
        responsed_data = response.json()
        album_items = responsed_data.get('items')
        album_ids = [album.get('id') for album in album_items]
        for album_id in album_ids :
            get_album_tracks(album_id)
    
    elif response_code == 401 :
        print(f'get_artist_albums(artist_id={artist_id}) - 토큰만료오류')
    elif response_code == 404 :
        print(f'get_artist_albums(artist_id={artist_id}) - 리퀘스트오류')
    else : print(f'get_artist_albums(artist_id={artist_id}) - {response.status_code}')

def get_album_tracks(album_id:str,limit:int=50,offset:int=0) :
    response = requests.get(f'https://api.spotify.com/v1/albums/{album_id}/tracks'
                            +'?limit={}&offset={}'.format(limit,offset)
                            ,headers=search_header)
    response_code = response.status_code
    if response_code == 200 :
        responsed_data = response.json()
        track_items = responsed_data.get('items')
        track_ids = [track.get('id') for track in track_items]

        tracks_data = [search_by_id('track',id) for id in track_ids]
        tracks = [Spotify.TracksORM(track) for track in tracks_data]

        audios = list()
        for track_id in track_ids :
            audios.append(Spotify.AudioFeaturesORM(get_audio_features(track_id)))

        with DB.session_scope() as session :
            session.add_all(tracks)
            session.add_all(audios)

    elif response_code == 401 :
        print(f'get_album_tracks(album_id={album_id}) - 토큰만료오류')
    elif response_code == 404 :
        print(f'get_album_tracks(album_id={album_id}) - 리퀘스트오류')
    else : print(f'get_album_tracks(album_id={album_id}) - {response.status_code}')

def search_by_keywords(keywords:str,type:list[str]=['artist','album','track'],limit:int=3,offset:int=0) :
    response = requests.get('https://api.spotify.com/v1/search'
                            +'?q={}'.format(keywords)
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
        print(f'search_by_keywords(keywords={keywords}) - 토큰만료오류')
    elif response_code == 404 :
        print(f'search_by_keywords(keywords={keywords}) - 리퀘스트오류')
    else : print(f'search_by_keywords(keywords={keywords}) - {response.status_code}')

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
        print(f'search_by_query(type={type}, keywords={keywords}) - 토큰만료오류')
    elif response_code == 404 :
        print(f'search_by_query(type={type}, keywords={keywords}) - 리퀘스트오류')
    else : print(f'search_by_query(type={type}, keywords={keywords}) - {response.status_code}')

def search_by_id(type:str,id:str) :
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
        print(f'search_by_id({type}s/{id}) - 토큰만료오류')
    elif response_code == 404 :
        print(f'search_by_id() - 리퀘스트오류')
    else : print(f'search_by_id({type}s/{id}) - {response.status_code}')

def search_by_href(href:str) :
    parsed_url = urlparse(href)
    if not parsed_url.query :
        path_params = parsed_url.path.split('/')
        type = path_params[-2][:-1]
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

def cull_data(parsed_data:Spotify.SearchTracks) :
    tracks_data = parsed_data.items

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
                        id=track.id
                        ,album_id=track.album.id
                        ,name=track.name
                        ,img=track.album.images[0].url if hasattr(track.album,'images') and track.album.images and track.album.images[0].url else None
                        ,artist=', '.join([artist.name for artist in track.artists])
                        ,duration=convert_timestamp(int(track.duration_ms))
                    ) for track in tracks]
    albums_result = [Meta.Album(
                        id=album.id
                        ,name=album.name
                        ,img=album.images[0].url if hasattr(album,'images') and album.images and album.images[0].url else None
                        ,artist=', '.join([artist.name for artist in album.artists])
                        ,release_year=album.release_date
                    ) for album in albums]
    artists_result = [Meta.Artist(
                        id=artist.id
                        ,name=artist.name
                        ,img=artist.images[0].url if hasattr(artist,'images') and artist.images and artist.images[0].url else None
                    ) for artist in artists]
    
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
    
    func_lyric(search_result.tracks)

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
        print(f'get_audio_features(track_id={track_id}) - 토큰만료오류')
    elif response_code == 404 :
        print(f'get_audio_features(track_id={track_id}) - 리퀘스트오류')
    else : print(f'get_audio_features() - {response.status_code}')

def func_lyric(tracks_data:list[Spotify.TracksORM]):
    import src.lyric as Lyric
    import src.lyrics_analyze as Analyze
    for track in tracks_data :
        Lyric.lyric_search_and_input(
            track_id=track.id, track=track.name, artist=','.join([artist.name for artist in track.artists])
            , GENIUS_API_KEY=Lyric.GENIUS_API_KEY)
    # with DB.engine.connect() as con :
    #     res = con.execute(DB.text('''
    #                                 SELECT tr.id, tr.name, string_agg(DISTINCT ta."name"::TEXT,',') 
    #                                 FROM spotify_artists ta 
    #                                 LEFT JOIN spotify_tracks tr ON ta.id = any(tr.artists_ids)
    #                                 LEFT JOIN lyrics lr ON lr.id = tr.id
    #                                 WHERE lr."content" IS NULL AND tr.id IS NOT NULL AND tr.name IS NOT null
    #                                 GROUP BY tr.id, tr.name
    #                               ''')).fetchall()
    #     for row in res :
    #         track_id, track_name, artist_names = row[0], row[1], row[2]
    #         Lyric.lyric_search_and_input(track_id=track_id,track=track_name,artist=artist_names
    #                                      , GENIUS_API_KEY=Lyric.GENIUS_API_KEY)
    Analyze.lyrics_analyze()

if __name__ == '__main__' :
    pass