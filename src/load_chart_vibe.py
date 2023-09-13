import requests
import re
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import urllib.parse
from model.chart_vibe import VibeEntity, VibeORM, ArtistInfo, Vibe_Load, ArtistInfo
from model.database import session_scope
from update_token import return_token

access_token = return_token()

def clean_name(name:str) :
    decoded_name = urllib.parse.unquote(name)
    normalized_name = re.sub(r'\([^)]*\)', '', decoded_name).strip()
    return normalized_name

def clean_track(name:str) :
    name = clean_name(name)
    if name == '이브, 프시케 그리고 푸른 수염의 아내':
        return 'Eve, Psyche & The Bluebeard’s wife'
    elif name == 'Seven  - Clean Ver.':
        return 'Seven (feat. Latto) (Clean Ver.)'
    elif name == '사람 Pt.2 ':
        return 'People Pt.2 (feat. IU)'
    elif name == '그대만 있다면 )':
        return '그대만 있다면'
    else : return name

def clean_album(name:str) :
    name = clean_name(name)
    return name

def clean_artists(artists:list[ArtistInfo]) :
    for original in artists :
        original.artistName = clean_name(original.artistName)
        if original.artistName == '미연아이들)':
            original.artistName = '미연'
        elif original.artistName == '#안녕':
            original.artistName = urllib.parse.quote(original.artistName)
        # elif original.artistName == '헤이즈 , 정승환':
        #     original.artistName = '헤이즈'
    return artists

def func1() :
    _USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    _ACCEPT = "application/json"
    _CHART_API_URL = "https://apis.naver.com/vibeWeb/musicapiweb/vibe/v1/chart/track/total"

    headers = {
        "User-Agent": _USER_AGENT,
        "Accept": _ACCEPT
    }

    queryStart = int(1)
    queryCount = int(100)
    
    response = requests.get(
        f"{_CHART_API_URL}?start={queryStart}&display={queryCount}",
        headers=headers
    )

    if response.status_code == 200 :
        responsed_data = response.json().get('response').get('result').get('chart').get('items')
        
        parsed_data = Vibe_Load(**responsed_data)
        vibes = parsed_data.tracks
        
        for vibe in vibes :
            vibe.trackTitle = clean_track(vibe.trackTitle)
            vibe.album.albumTitle = clean_album(vibe.album.albumTitle)
            vibe.artists = clean_artists(vibe.artists)
    
        return vibes

def func2(vibe:VibeEntity):
    from src.get_token import return_token, update_token
    access_token = update_token('iamsophie')

    import model.spotify_search as Spotify
    q = vibe.trackTitle+' '+', '.join([artist.artistName for artist in vibe.artists])
    print(q)
    url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
    headers = {
        'Authorization': 'Bearer '+access_token
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        responsed_data = response.json().get('tracks')
        
        parsed_data = Spotify.SearchTracks(**responsed_data)
        tracks = parsed_data.items
        track = tracks.pop()

        vibe.trackTitle = track.name
        vibe.album.albumTitle = track.album.name
        vibe.album.imageUrl = track.album.images[0].url
        for i, artist in enumerate(vibe.artists) :
            try :
                artist.artistName = track.artists[i].name
            except IndexError as e :
                artist.artistName = None
        
        return vibe

if __name__ == '__main__':

        vibes_before = func1()  
        vibes_after = [VibeORM(func2(vibe_before)) for vibe_before in vibes_before]

        with session_scope() as session :
            session.add_all(vibes_after)
            
        # for index, item in enumerate(responsed_data):
        #     artist_names = []
        #     # artist_ids = []

        #     pre_track_title = item['trackTitle']
        #     parse_track_title = urllib.parse.unquote(pre_track_title)
        #     cleaned_track = re.sub(r'\([^)]*\)', '', parse_track_title)

        #     # 예외 처리
        #     if cleaned_track == '이브, 프시케 그리고 푸른 수염의 아내':
        #         cleaned_track = 'Eve, Psyche & The Bluebeard’s wife'
        #     elif cleaned_track == 'Seven  - Clean Ver.':
        #         cleaned_track ='Seven (feat. Latto) (Clean Ver.)'
        #     elif cleaned_track == '사람 Pt.2 ':
        #         cleaned_track = 'People Pt.2 (feat. IU)'
            
        #     pre_album = item['album']['albumTitle']
        #     parse_album = urllib.parse.unquote(pre_album)
        #     cleaned_album = re.sub(r'\([^)]*\)', '', parse_album)
            
        #     artists = item.get('artists')
            
        #     for artist in artists:
        #         pre_artist = artist['artistName']
        #         # artist_id = artist['artistId']
        #         parse_artist = urllib.parse.unquote(pre_artist)  # URL 디코딩
        #         cleaned_artist = re.sub(r'\([^)]*\)', '', parse_artist)
        #         if cleaned_artist == '미연아이들)':
        #             cleaned_artist = '미연'
        #         elif cleaned_artist == '#안녕':
        #             cleaned_artist = urllib.parse.quote(pre_artist)
        #         artist_names.append(cleaned_artist)
        #         # artist_ids.append(artist_id)
            
        #     q = cleaned_track + " " + ', '.join(artist_names)
        #     # print(q)
        #     url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
        #     headers = {
        #         'Authorization': 'Bearer '+access_token
        #     }
        #     response_sp = requests.get(url, headers=headers)
        #     if response_sp.status_code == 200:
        #         sp_json = response_sp.json()
        #         artists_sp_nm = []
        #         item['trackTitle'] = sp_json['tracks']['items'][0]['name']
        #         item['album']['albumTitle'] = sp_json['tracks']['items'][0]['album']['name']
        #         item['album']['imageUrl'] = sp_json['tracks']['items'][0]['album']['images'][0]['url']
        #         for j in range(len(sp_json['tracks']['items'][0]['artists'])):
        #             item['artists'][0]['artistName'] = sp_json['tracks']['items'][0]['artists'][j]['name']
        #             # item['artists'][j]['artistName'] = ', '.join(artists_sp_nm)
        #         # print(item['artists'][0]['artistName'])
        #     entity = VibeEntity(**item)
        #     # print([e.artistName for e in entity.artists if e.artistName == ])
        #     orm = VibeORM(entity)

        #     with session_scope() as session :
        #         session.add(orm)