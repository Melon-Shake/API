import requests
import re
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import urllib.parse
from model.chart_vibe import VibeEntity, VibeORM, ArtistInfo
from model.database import session_scope
from update_token import return_token

access_token = return_token()

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
        # print(responsed_data[12])

        for index, item in enumerate(responsed_data):
            artist_names = []
            # artist_ids = []
            pre_track_title = item['trackTitle']
            parse_track_title = urllib.parse.unquote(pre_track_title)
            cleaned_track = re.sub(r'\([^)]*\)', '', parse_track_title)
            # 예외 처리
            if cleaned_track == '이브, 프시케 그리고 푸른 수염의 아내':
                cleaned_track = 'Eve, Psyche & The Bluebeard’s wife'
            elif cleaned_track == 'Seven  - Clean Ver.':
                cleaned_track ='Seven (feat. Latto) (Clean Ver.)'
            elif cleaned_track == '사람 Pt.2 ':
                cleaned_track = 'People Pt.2 (feat. IU)'
            
            pre_album = item['album']['albumTitle']
            parse_album = urllib.parse.unquote(pre_album)
            cleaned_album = re.sub(r'\([^)]*\)', '', parse_album)
            
            artists = item.get('artists')
            
            for artist in artists:
                pre_artist = artist['artistName']
                # artist_id = artist['artistId']
                parse_artist = urllib.parse.unquote(pre_artist)  # URL 디코딩
                cleaned_artist = re.sub(r'\([^)]*\)', '', parse_artist)
                if cleaned_artist == '미연아이들)':
                    cleaned_artist = '미연'
                elif cleaned_artist == '#안녕':
                    cleaned_artist = urllib.parse.quote(pre_artist)
                artist_names.append(cleaned_artist)
                # artist_ids.append(artist_id)
            
            q = cleaned_track + " " + ', '.join(artist_names)
            # print(q)
            url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
            headers = {
                'Authorization': 'Bearer '+access_token
            }
            response_sp = requests.get(url, headers=headers)
            if response_sp.status_code == 200:
                sp_json = response_sp.json()
                artists_sp_nm = []
                item['trackTitle'] = sp_json['tracks']['items'][0]['name']
                item['album']['albumTitle'] = sp_json['tracks']['items'][0]['album']['name']
                item['album']['imageUrl'] = sp_json['tracks']['items'][0]['album']['images'][0]['url']
                for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                    item['artists'][0]['artistName'] = sp_json['tracks']['items'][0]['artists'][j]['name']
                    # item['artists'][j]['artistName'] = ', '.join(artists_sp_nm)
                # print(item['artists'][0]['artistName'])
            entity = VibeEntity(**item)
            # print([e.artistName for e in entity.artists if e.artistName == ])
            orm = VibeORM(entity)

            with session_scope() as session :
                session.add(orm)