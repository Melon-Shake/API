import re
import requests
import sys

import os, urllib.parse
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from get_token import return_token
from model.chart_genie import ChartGenie, GenieORM
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
            pre_track_title = item['SONG_NAME']
            pre_track_title = pre_track_title.replace("-", "")
            pre_track_title = pre_track_title.replace("Prod. by", "Prod.")
            pre_track_title = urllib.parse.unquote(pre_track_title)
            
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
           
            pre_artists = item.get('ARTIST_NAME')
            pre_artists = urllib.parse.unquote(pre_artists)
            if pre_artists == '#안녕':
                pre_artists = urllib.parse.quote(pre_artists)# URL 디코딩
            artists = pre_artists.split(' & ')
            artists = ','.join(artists)
            
            pre_album = item['ALBUM_NAME']
            album = urllib.parse.unquote(pre_album)
            
            entries[index] = [pre_track_title, artists, album]

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
 

    for idx, e in enumerate(responsed_data) :
        entity = ChartGenie(**e)
        orm = GenieORM(entity)
        orm.track_name = song_name[idx]
        orm.track_id = song_ids[idx]
        orm.artist_names = ','.join(artist_name[idx])
        orm.artist_ids = artist_ids[idx]
        orm.album_name = album_name[idx]
        orm.album_id = album_ids[idx]
        orm.img_url = album_img[idx]

        with session_scope() as session :
            session.add(orm)