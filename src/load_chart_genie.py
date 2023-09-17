import re
import requests
import sys

import os, urllib.parse
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from update_token import return_token
from model.chart_genie import ChartGenie , ChartGenieORM
from model.database import session_scope

access_token = return_token()

if __name__ == '__main__' :
    response = requests.post('https://app.genie.co.kr/chart/j_RealTimeRankSongList.json'
                             ,headers={
                                 'Content_Type' : 'application/x-www-form-urlencoded'
                             }
                             ,data={
                                'pgSize': '100'
                             }
                            )

    if response.status_code == 200 :
        responsed_data = response.json().get('DataSet').get('DATA')
        
        song_name = []
        song_ids = []
        artist_name = []
        artist_ids = []
        album_name = []
        album_ids = []
        album_img = []

        entries = {}
        for index, item in enumerate(responsed_data):
            # 제목 디코딩
            pre_track_title = item['SONG_NAME']
            track_title = urllib.parse.unquote(pre_track_title)
            cleaned_track = re.sub(r'\([^)]*\)', '', track_title)
            
            # 예외 처리
            if cleaned_track == '이브, 프시케 그리고 푸른 수염의 아내':
                cleaned_track = 'Eve, Psyche & The Bluebeard’s wife'
                
            if track_title == '건물 사이에 피어난 장미 (Rose Blossom)':
                track_title = 'Rose Blossom'
                
            if track_title == '해요 (2022)':
                track_title = 'haeyo 2022'
           
            # 아티스트 디코딩
            pre_artists = item.get('ARTIST_NAME')
            artists = urllib.parse.unquote(pre_artists) 
            cleaned_artist = re.sub(r'\([^)]*\)', '', artists)
            
            #예외 처리
            if cleaned_artist == '#안녕':
                cleaned_artist = urllib.parse.quote(pre_artists)
                
            # 앨범제목
            pre_album = item['ALBUM_NAME']
            album = urllib.parse.unquote(pre_album)
            
            entries[index] = [cleaned_track, cleaned_artist, cleaned_album]

    for i in range(len(entries)):
        
        q = entries[i][0] + " " + entries[i][1]

        url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
        headers = {
            'Authorization': 'Bearer '+access_token
        }
        response_sp = requests.get(url, headers=headers)
        if response_sp.status_code == 200:
            sp_json = response_sp.json()
            artists_sp = []
            artist_id = []
            song_name.append(sp_json['tracks']['items'][0]['name'])
            song_ids.append(sp_json['tracks']['items'][0]['id'])
            album_name.append(sp_json['tracks']['items'][0]['album']['name'])
            album_ids.append(sp_json['tracks']['items'][0]['album']['id'])
            album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
            
            for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
                artist_id.append(sp_json['tracks']['items'][0]['artists'][j]['id'])
            artist_name.append(artists_sp)
            artist_ids.append(artist_id)
 
 
    # print(song_name[0])
    # print(artist_name[0])
    # print(album_name[0])
    # print(album_img[0])

    for idx, e in enumerate(responsed_data) :
        entity = ChartGenie(**e)
        orm = ChartGenieORM(entity)

        with session_scope() as session :
            session.add(orm)