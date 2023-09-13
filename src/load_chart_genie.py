import re
import requests
import sys

import os, urllib.parse
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from update_token import return_token
from model.chart_genie import ChartGenie, ChartGenieORM
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
        artist_name = []
        album_name = []
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
           
            # 아티스트 디코딩
            pre_artists = item.get('ARTIST_NAME')
            artists = urllib.parse.unquote(pre_artists)  # URL 디코딩
            cleaned_artist = re.sub(r'\([^)]*\)', '', artists)
            #예외 처리
            if cleaned_artist == '#안녕':
                cleaned_artist = urllib.parse.quote(pre_artists)
            # 앨범제목
            pre_album = item['ALBUM_NAME']
            album = urllib.parse.unquote(pre_album)
            cleaned_album = re.sub(r'\([^)]*\)', '', album)
            
            entries[index] = [cleaned_track, cleaned_artist, cleaned_album]
        # print(responsed_data)

    for i in range(len(entries)):
        
        q = entries[i][0] + " " + entries[i][1]
        print(q)
        url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
        headers = {
            'Authorization': 'Bearer '+access_token
        }
        response_sp = requests.get(url, headers=headers)
        if response_sp.status_code == 200:
            sp_json = response_sp.json()
            artists_sp = []
            song_name.append(sp_json['tracks']['items'][0]['name'])
            album_name.append(sp_json['tracks']['items'][0]['album']['name'])
            album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
            
            for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
            artist_name.append(', '.join(artists_sp))
        elif response_sp.status_code != 200 :
            q = entries[i][0] + " " + entries[i][1]+ " " + entries[i][2]
            url = f'https://api.spotify.com/v1/search?q={q}&type=track&market=KR&limit=1'
            headers = {
                'Authorization': 'Bearer '+access_token
            }
            response_sp = requests.get(url, headers=headers)
            if response_sp.status_code == 200:
                sp_json = response_sp.json()
                artists_sp = []
                song_name.append(sp_json['tracks']['items'][0]['name'])
                album_name.append(sp_json['tracks']['items'][0]['album']['name'])
                album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                
                for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                    artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
                artist_name.append(', '.join(artists_sp))
    # for i in range(len(responsed_data)):
        responsed_data[i]['SONG_NAME'] = song_name[i]
        responsed_data[i]['ARTIST_NAME'] = artist_name.pop()
        responsed_data[i]['ALBUM_NAME'] = album_name[i]
        responsed_data[i]['ALBUM_IMG_PATH'] = album_img[i]
        # elseif response_sp.status_code == 400:
        #     print(f'{i} : {response_sp.status_code}')
        
        # print(responsed_data)

    for e in responsed_data :
        entity = ChartGenie(**e)
        orm = ChartGenieORM(entity)

        with session_scope() as session :
            session.add(orm)

    else : print(response.status_code)
    
    

# 원래 문자열
# original_string = "Smoke (Prod. by Dynamicduo & Padi) 심(心)"

# # 정규 표현식을 사용하여 괄호와 괄호 안의 내용을 제거
# cleaned_string = re.sub(r'\([^)]*\)', '', original_string)

# # 결과 출력
# print(cleaned_string)
