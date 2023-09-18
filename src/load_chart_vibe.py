import requests
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import urllib.parse
from model.chart_vibe import VibeEntity, VibeORM, ArtistInfo, Vibe_Load, ArtistInfo
import urllib.parse
from model.chart_vibe import VibeEntity, VibeORM
from model.database import session_scope
from get_token import return_token

access_token = return_token()

# def clean_name(name:str) :
#     decoded_name = urllib.parse.unquote(name)
#     normalized_name = decoded_name.replace("-", "")
#     normalized_name = normalized_name.replace("Prod. by", "Prod.")
#     return normalized_name

# def clean_track(name:str) :
#     name = clean_name(name)
#     if name == '이브, 프시케 그리고 푸른 수염의 아내':
#         name = 'Eve, Psyche & The Bluebeard’s wife'
#     elif name == '파이팅 해야지 (Feat. 이영지)':
#         name ='Fighting'
#     elif name == '손오공':
#         name ='Super'
#     elif name == '사람 Pt.2 ':
#         name = 'People Pt.2 (feat. IU)'
#     elif name == '사람 Pt.2 (feat. 아이유)':
#         name = 'People Pt.2 (feat. IU)'
#     elif name == 'STAY (Explicit Ver.)':
#         name = 'STAY'
#     else : return name

# def clean_album(name:str) :
#     name = clean_name(name)
#     return name

# def clean_artists(artists:list[ArtistInfo]) :
#     for original in artists :
#         original.artistName = clean_name(original.artistName)
#         if original.artistName == '#안녕':
#             original.artistName = urllib.parse.quote(original.artistName)
#     return artists

# def func1() :
#     _USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
#     _ACCEPT = "application/json"
#     _CHART_API_URL = "https://apis.naver.com/vibeWeb/musicapiweb/vibe/v1/chart/track/total"

#     headers = {
#         "User-Agent": _USER_AGENT,
#         "Accept": _ACCEPT
#     }

#     queryStart = int(1)
#     queryCount = int(100)
    
#     response = requests.get(
#         f"{_CHART_API_URL}?start={queryStart}&display={queryCount}",
#         headers=headers
#     )

#     if response.status_code == 200 :
#         responsed_data = response.json().get('response').get('result').get('chart').get('items')
        
#         parsed_data = Vibe_Load(**responsed_data)
#         vibes = parsed_data.tracks
        
#         for vibe in vibes :
#             vibe.trackTitle = clean_track(vibe.trackTitle)
#             vibe.album.albumTitle = clean_album(vibe.album.albumTitle)
#             vibe.artists = clean_artists(vibe.artists)
    
#         return vibes

# def func2(vibe:VibeEntity):
#     from src.get_token import return_token, update_token
#     access_token = update_token('iamsophie')

#     import model.spotify_search as Spotify
#     q = vibe.trackTitle+' '+', '.join([artist.artistName for artist in vibe.artists])
#     print(q)
#     url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
#     headers = {
#         'Authorization': 'Bearer '+access_token
#     }
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         responsed_data = response.json().get('tracks')
        
#         parsed_data = Spotify.SearchTracks(**responsed_data)
#         tracks = parsed_data.items
#         track = tracks.pop()

#         vibe.trackTitle = track.name
#         vibe.album.albumTitle = track.album.name
#         vibe.album.imageUrl = track.album.images[0].url
#         for i, artist in enumerate(vibe.artists) :
#             try :
#                 artist.artistName = track.artists[i].name
#             except IndexError as e :
#                 artist.artistName = None
        
#         return vibe


if __name__ == '__main__':

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
        responsed_data = response.json().get('response').get('result').get('chart').get('items').get('tracks')
        song_name = []
        song_ids = []
        artist_name = []
        artist_ids = []
        album_name = []
        album_ids = []
        album_img = []
        # print(responsed_data[0])
        # print(responsed_data[0])
        entries = {}
        
        
        for index, item in enumerate(responsed_data):
            e = VibeEntity(**item)
            e.trackTitle
            e.album.albumTitle
            e.album.imageUrl
            e.artists
            e = VibeEntity(**item)
            e.trackTitle
            e.album.albumTitle
            e.album.imageUrl
            e.artists
            
            pre_track_title = e.trackTitle
            pre_track_title = pre_track_title.replace("-", "")
            pre_track_title = pre_track_title.replace("Prod. by", "Prod.")

            pre_track_title = e.trackTitle
            pre_track_title = pre_track_title.replace("-", "")
            pre_track_title = pre_track_title.replace("Prod. by", "Prod.")
            pre_track_title = urllib.parse.unquote(pre_track_title)

            # 예외 처리
            if pre_track_title == '이브, 프시케 그리고 푸른 수염의 아내':
                pre_track_title = 'Eve, Psyche & The Bluebeard’s wife'
            elif pre_track_title == '파이팅 해야지 (Feat. 이영지)':
                pre_track_title ='Fighting'
            elif pre_track_title == '손오공':
                pre_track_title ='Super'
            elif pre_track_title == '사람 Pt.2 ':
                pre_track_title = 'People Pt.2 (feat. IU)'
            elif pre_track_title == '사람 Pt.2 (feat. 아이유)':
                pre_track_title = 'People Pt.2 (feat. IU)'
            elif pre_track_title == 'STAY (Explicit Ver.)':
                pre_track_title = 'STAY'
            
            pre_album = e.album.albumTitle
            parse_album = urllib.parse.unquote(pre_album)
            if pre_track_title == '이브, 프시케 그리고 푸른 수염의 아내':
                pre_track_title = 'Eve, Psyche & The Bluebeard’s wife'
            elif pre_track_title == '파이팅 해야지 (Feat. 이영지)':
                pre_track_title ='Fighting'
            elif pre_track_title == '손오공':
                pre_track_title ='Super'
            elif pre_track_title == '사람 Pt.2 ':
                pre_track_title = 'People Pt.2 (feat. IU)'
            elif pre_track_title == '사람 Pt.2 (feat. 아이유)':
                pre_track_title = 'People Pt.2 (feat. IU)'
            elif pre_track_title == 'STAY (Explicit Ver.)':
                pre_track_title = 'STAY'
            
            pre_album = e.album.albumTitle
            parse_album = urllib.parse.unquote(pre_album)
            
            for artist in pre_artist:
                artist_nm = artist['artistName']
                artists = urllib.parse.unquote(artist_nm)
                cleaned_artist = re.sub(r'\([^)]*\)', '', artists)
                artist_pre.append(cleaned_artist)
                
                if artist_nm == '#안녕':
                    artists = urllib.parse.quote(artist_nm)
                    
                artist_pre.append(artists)
            
            # 앨범 제목
            pre_album = item['album']['title']
            album = urllib.parse.unquote(pre_album)
            cleaned_album = re.sub(r'\([^)]*\)', '', album)

            artist_pre.append(artist_nm)
            entries[index] = [track_title, artist_pre, album_title]
        # for x in responsed_data :
        #     entity = VibeEntity(**x)
        #     orm = VibeORM(entity)

        #     with session_scope() as session :
        #         session.add(orm)