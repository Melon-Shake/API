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
        # lyric_search_and_input(
        #     track_id=track.id
        #     ,track=track.name
        #     ,artist=', '.join([artist.name for artist in track.artists])
        #     ,GENIUS_API_KEY=GENIUS_API_KEY
        # )
    # lyrics_analyze()
    with db.session_scope() as session :
        session.add_all(audios)

    # audio_features_update()


if __name__ == '__main__' :
#     track_ids = [
#         '1qosh64U6CR5ki1g1Rf2dZ',
# '5Avril3IZ26DPVFHbJX8o6',
# '1qRfAvzRIJQodWKBNFAb6C',
# '56v8WEnGzLByGsDAXDiv4d',
# '5sdQOyqq2IDhvmx2lHOpwd',
# '6f4CAdAmrOfGH3FOfwHMSV',
# '2rj6rzz1qLMrZf8yWFwp9r',
# '50Q0BUdTTtaMumIELoyrm8',
# '7KavHYqoVFNB3IUXfs5gvP',
# '68r87x3VZdAMhv8nBVuynz',
# '7M3POeMOBCs6pwtDkVhBTi',
# '4P5ozkI1bxiGxA5rZ27jlO',
# '0a4MMyCrzT0En247IhqZbD',
# '0pHylQR53epYtRcVIhUSCh',
# '4QhnNyKDsAkXPwHkSnuc89',
# '4rMEoXVYww6Xy7q9wSj4gy',
# '1ULdASrNy5rurl1TZfFaMP',
# '2jidjmWNeRmKgLjXhW52Gz',
# '4WUpMUjdoi47LY7gBQBXe3',
# '3r8RuvgbX9s7ammBn07D3W',
# '2RLdkXSaiQjRbey5pvP8Kt',
# '0zWuvPDqBa0WM9Ffwl0rgb',
# '6R5fYCySNHrqo4Og6O1ppn',
# '4zCcKPm03kHARVAiyzlDX8',
# '6rdkCkjk6D12xRpdMXy0I2',
# '50xSycnGMDy0Wg5jJcOv3S',
# '365znJ27Fb3faGsctmQYWR',
# '6auT8cRBu3BgPRBrdVBY15',
# '26Iv7VGUF1lqU10rxQXFL8',
# '6RBziRcDeiho3iTPdtEeg9',
# '2tA3NP12r4niSRhb9Y6AoY',
# '3BlFzuu8yqE4bMrHKTViee',
# '51vRumtqbkNW9wrKfESwfu',
# '6CV6j2xz54thzlrWML3kAW',
# '1E14FuM0BRaHAJSJ9YxMVu',
# '4Cr43xPo7bwyCcL1g3yVCu',
# '2pIUpMhHL6L9Z5lnKxJJr9',
# '7x3SGAkfIrzDr9paSslwMv',
# '65FftemJ1DbbZ45DUfHJXE',
# '24hyxhmnwutr6ncxX9ALIU',
# '2lsRp40mCRkhqULWdMbOzn',
# '0yfQBmmOIVqiwhV5u10EhN',
# '0Q5VnK2DYzRyfqQRJuUtvi',
# '1BuA7GJXWD6P9LMShz7YSt',
# '05STjz8kmPBUebu3uu5sO0',
# '0eFMbKCRw8KByXyWBw8WO7',
# '3iLBFgaQJ94iarMgzrTuWb',
# '4YTvuLSqKshDOJvwyDmAYS',
# '6GukZESVRKPnnz4vZGUNxC',
# '3AOf6YEpxQ894FmrwI9k96',
# '0bC7GKnxh9W9JIvJ6HVWxc',
# '2N0SPREDYqILVEFSsWF5N5',
# '4kSDi21MeOoSvpZs6MveI9',
# '72wqLtMtkrB0qUw6jSqM0Z',
# '2X45nVBeYzmDlrXji9Av0Q',
# '3uzUBVCNTdVnmJMumFA4Ce',
# '3qonjOrhFCfTnaaMruHzxW',
# '1Xnha5ko8j7yY8O3ATe0Vs',
# '02wk5BttM0QL38ERjLPQJB',
# '5mdl3TlXrImNPrIo3aO70q',
# '7eBpUuPnDTfbeP1P4P93CS',
# '4fsQ0K37TOXa3hEQfjEic1',
# '0hqngwyh8WnPuYlLYHRQqp',
# '5IAESfJjmOYu7cHyX557kz',
# '5h1BN75CEh8wdSwE1xrbSe',
# '29j6SXQOmfSbiemMriO25W',
# '0hqj5JBnFt1BHEz2UCFwrl',
# '5ydjxBSUIDn26MFzU3asP4',
# '6jjYDGxVJsWS0a5wlVF5vS',
# '0tgxvf4rqBBeEB54h0nnRD',
# '16LATbHXLu0gh8MCw1hUGl',
# '5HCyWlXZPP0y6Gqq8TgA20',
# '5grkkSqOpUGHfl2KunfdD9',
# '1RDvyOk4WtPCtoqciJwVn8',
# '3TUPqVuyNK2mPeA9QmHygo',
# '7FrabSVdfcPggA25gq3LJU',
# '3Ua0m0YmEjrMi9XErKcNiR',
# '5BqwC9kOBbqYkzdOKeXFFk',
# '3fR9cyHIKckUDwuy3m5tKn',
# '0YQEptsxR8l60SgOn3BZ5P',
# '5gst02IN8JD3CfXM7IfVnc',
# '5bdmWBCaiaHk2HbqKOXLyJ',
# '5164wquGnyhOYN0JiHYhQO',
# '4EaQ0ouIydfeAgQUz284EF',
# '0M4EDkH7RpbKlWwrZ9o17N',
# '7FbrGaHYVDmfr7KoLIZnQ7',
# '27bIik73QCu8Xzt3xpG1bI',
# '6JIm38KbaDGfi65VGETDi9',
# '0wPKDeY4fZXT6k9bzV0kx0',
# '6WYsZJDfUOftGVji74yYSU',
# '5fpyAakgFOm4YTXkgfPzvV',
# '1z4mivQugjaobIZAqR4N4U',
# '7n2FZQsaLb7ZRfRPfEeIvr',
# '0UnOf7i44YK0ULpkEGHe4R',
# '5f2CcxzZoW7hNs1O8NhG6y',
# '3Ml2s37uS9jqRM2R3bfDiB',
# '71DQGd44Wyie6hJu1yBzdQ',
# '775S83AMYbQc8SYteOktTL',
# '0CB3B5ir8I2KbB3dkGVtWF',
# '3eOXiUUfz9OhyVqoREsJYe',
# '6tohHT5sQRMjdWHMNn190u',
# '6zZWoHlF2zNSLUNLvx4GUl',
# '5wxYxygyHpbgv0EXZuqb9V',
# '7tOsgOjrzBVQqyaMDBlZV8',
# '6j268AN4RJXNyFNeFUfB50',
# '7pYiTMBG8sgPJvXZZ476i1',
# '7Ejqkb9YfldcLoh8B6bXgj',
# '6tCd8bPvYnceDG7W9M1RMk',
# '1q9TLiBIGcjEchuhPSIz8c',
# '3P3UA61WRQqwCXaoFOTENd',
# '4H65EdACzwqV8sTt3dDyA0',
# '3HAkoNmThZhyFejhpRXXYI',
# '10PzmnIzAwd4vRRDUamEwr',
# '1zOOl8f7qkjj0AmvlCfLyQ',
# '0afnaAYZk1IPQSFDd2MGw0',
# '1ckjVyV85YJob7nFZlEHIo',
# '2BgEsaKNfHUdlh97KmvFyo',
# '5P3o95Jf0YBQRQ4j2XPpfC',
# '4ZtFanR9U6ndgddUvNcjcG',
# '6KiEF5zqzHiFjzdm8gChz7',
# '7CHDUDw89DCR8vvI0yTXGa',
# '0EhdXt3y460mTRsi97Pyk5',
# '5mdWIwsJAzR97ShGkt8gcR',
# '0NoeYUnwpb9R26mpylHcR9',
# '0UXLLeFAFbo5JbSR9C4STe',
# '02SbQgZbzMoylPoGr32ugF',
# '7MXtr93z4ltQzhfIxYnYWX',
# '6nICBdDevG4NZysIqDFPEa',
# '6AB530RfPBhjaqikjc04Ay',
# '3Yzlsk9g1zqWZUeI5oq1BN',
# '7n4vU9BEfT1cEIiSWRg54K',
# '7egcmrxRDee6C5M3AtXZ7L',
# '2SCOjgC1DSu7XskVTo0Wzl',
# '2DwUdMJ5uxv20EhAildreg',
# '6262LmmRM1khHX1D4yk6MA',
# '3TQHPUEVdvdq8ejwEcHUlL',
# '296nXCOv97WJNRWzIBQnoj',
# '49KDK2ccYnOCYPeXfDO3YT',
# '3T03rPwlL8NVk1yIaxeD8U',
# '2BPXILn0MqOe5WroVXlvN1',
# '3F4lHPNHlvr3RpO4tpVOIs',
# '1rguO7AsN5jYbXr5POizxK',
# '29zCNlz61XPcShFxHyoTpM',
# '7ovUcF5uHTBRzUpB6ZOmvt',
# '2AlNztYMWRJOg13xhUGwOj',
# '2W8UduoifU1zgjKZlfY79S',
# '0D5e4R40frQYkr2PzdMpHL',
# '7rXcCpIAoOUCydkVDMcoPV',
# '4gaQqWAKoCxuisDNCFgj45',
# '2cGf0hmhkACTwRj58XNGlP',
# '6FZAc2XaVYc8G8jaDnBshv',
# '5TNMJ6Csb2NgSohuz76XJT',
# '5bN5cxUTmuiWrJbQogtA9c',
# '0HsRZwZzHoZ5AM5W2ZYI5c',
# '6WuPoxLfBk1mTSSPTa6WOJ',
# '0NiqekhsLPMtjTsJbOSRhG',
# '5jqSg1iJnSoYSjdsozWVOm',
# '4SQH8x0PnOqEWWgbAlXIXJ',
# '3kk4oPmTbAstqb2j1BFeKm',
# '03qu1u4hDyepQQi2lNxCka',
# '1oIhaSskG6qqjtQUOru4hi',
# '3cEri8HtxeuJdzEZp3N3j9',
# '143U6PbmoAwueT1lZGBLVS',
# '7x9aauaA9cu6tyfpHnqDLo',
# '2g0LdZQce9xlcHb1mBJyuz',
# '348NF6vX0Yh22xvH0EZEro',
# '4a0OYMqeBOGuzCPLg5SfWU',
# '64104XJ1QlSXdsMkZJ8tnd',
# '2VV1RIhTgeJ4PEMYz6TqDB',
# '1FBdX6uTlbunrv0bu3tFnF',
# '4RJHDWdfgBwc1WXdL2aWaj',
# '5g4bfDE2pbwIyKRSOLP2Vy',
# '7a86ARVnm366v2UY1z9Ak8',
# '54zRGA28tVRKRmFCpywWko',
# '4SFS7L4PyRyTPhYX7imEuz',
# '3gafQxekHAbM52PxdX9SDR'
#     ]
#     from model.audio_features import AudioFeaturesORM
#     audios =list()
#     for track_id in track_ids :
#         audios.append(AudioFeaturesORM(get_audio_features(track_id)))
#     with session_scope() as session :
#         session.add_all(audios)
    
    # keywords = '파이팅 해야지 (Feat. 이영지)'
    # keywords = 'YOU&I'
    # keywords = ["coin 아이유"]

    # for keyword in keywords :
    #     parsed_data = search_by_keywords(keywords)
    #     if type(parsed_data) == str : print('#################'+parsed_data)
    #     culled_data = cull_data(parsed_data)
    #     load_spotify(culled_data)
    #     bring_lucete(culled_data.tracks)