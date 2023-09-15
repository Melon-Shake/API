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
            pre_track_title = urllib.parse.unquote(pre_track_title)
            pre_track_title = pre_track_title.replace("-", "")
            pre_track_title = pre_track_title.replace("Prod. by", "Prod.")
            
            # 예외 처리
            if pre_track_title == '이브, 프시케 그리고 푸른 수염의 아내':
                pre_track_title = 'Eve, Psyche & The Bluebeard’s wife'
            elif pre_track_title == '파이팅 해야지 (Feat. 이영지)':
                pre_track_title ='Fighting'
            elif pre_track_title == '손오공':
                pre_track_title ='Super'
            elif pre_track_title == '사람 Pt.2 ':
                pre_track_title = 'People Pt.2 (feat. IU)'
            elif pre_track_title == 'STAY (Explicit Ver.)':
                pre_track_title = 'STAY'
           
            # 아티스트 디코딩
            pre_artists = item.get('ARTIST_NAME')
            pre_artists = urllib.parse.unquote(pre_artists)
            if pre_artists == '#안녕':
                pre_artists = urllib.parse.quote(pre_artists)# URL 디코딩
            artists = pre_artists.split(' & ')
            artists = ','.join(artists)
            
            # 앨범제목
            pre_album = item['ALBUM_NAME']
            album = urllib.parse.unquote(pre_album)
            
            entries[index] = [pre_track_title, artists, album]
        # print(entries)

    for i in range(len(entries)):
        
        q = entries[i][0] + " " + entries[i][1]
        # print(q)
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
            artist_name.append(artists_sp)
        # elif response_sp.status_code != 200 :
        #     q = entries[i][0] + " " + entries[i][1]+ " " + entries[i][2]
        #     url = f'https://api.spotify.com/v1/search?q={q}&type=track&market=KR&limit=1'
        #     headers = {
        #         'Authorization': 'Bearer '+access_token
        #     }
        #     response_sp = requests.get(url, headers=headers)
        #     if response_sp.status_code == 200:
        #         sp_json = response_sp.json()
        #         artists_sp = []
        #         song_name.append(sp_json['tracks']['items'][0]['name'])
        #         album_name.append(sp_json['tracks']['items'][0]['album']['name'])
        #         album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                
        #         for j in range(len(sp_json['tracks']['items'][0]['artists'])):
        #             artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
        #         artist_name.append(', '.join(artists_sp))
        
   
        # responsed_data[i]['SONG_NAME'] = song_name[i]
        # responsed_data[i]['ARTIST_NAME'] = artist_name.pop()
        # responsed_data[i]['ALBUM_NAME'] = album_name[i]
        # responsed_data[i]['ALBUM_IMG_PATH'] = album_img[i]
 
    print(song_name[0])
    print(artist_name[0])
    print(album_name[0])
    print(album_img[0])

    for idx, e in enumerate(responsed_data) :
        entity = ChartGenie(**e)
        orm = ChartGenieORM(entity)
        orm.track_name = song_name[idx]
        orm.artist_names = artist_name[idx]
        orm.album_name = album_name[idx]
        orm.img_url = album_img[idx]

        with session_scope() as session :
            session.add(orm)