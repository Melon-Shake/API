import requests
import sys
import os, urllib.parse, re
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from update_token import return_token
from model.chart_bugs import BugsEntity, BugsORM
from model.database import session_scope

access_token = return_token()

if __name__ == '__main__':

    _USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    _IMAGE_PREFIX_URL = "https://image.bugsm.co.kr/album/images"
    _CHART_API_URL = "https://m.bugs.co.kr/api/getChartTrack"

    headers = {
        "User-Agent": _USER_AGENT,
    }

    Domestic = 20152 # 국내차트 - 20152
    Realtime = 'realtime' # 시간별차트
    headers = {"User-Agent": _USER_AGENT}
    data = {"svc_type": Domestic, "period_tp": Realtime,"size":100,}
    response = requests.post(_CHART_API_URL, headers=headers, data=data)
    
    if response.status_code == 200 :
        responsed_data = response.json().get('list')
        song_name = []
        artist_name = []
        album_name = []
        album_img = []

        entries = {}
        for index, item in enumerate(responsed_data):
            
            # 제목 디코딩
            pre_track_title = item['track_title']
            pre_track_title = pre_track_title.replace("-", "")
            pre_track_title = pre_track_title.replace("Prod. by", "Prod.")
            track_title = urllib.parse.unquote(pre_track_title)

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

            
        #     # 아티스트 디코딩
            pre_artists = item.get('artists')
            artist_pre = []
            for artist in pre_artists:
                artist_nm = artist['artist_nm']
                if artist_nm == '#안녕':
                    artist_nm = urllib.parse.quote(artist_nm)
                artist_pre.append(artist_nm)
            artists = ','.join(artist_pre)
            
            # 앨범제목    
            pre_album = item['album']['title']
            album = urllib.parse.unquote(pre_album)
            
            entries[index] = [pre_track_title, artists, pre_album]
                    
        for i in range(len(entries)):
            # artists_sub = ' '.join(entries[i][1])
            q = entries[i][0] +' '+ entries[i][1]
            # print(q,i)
            url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
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
        #     elif response_sp.status_code != 200 :
        #         q = entries[i][0] + " " + artists_sub+ " " + entries[i][2]
        #         url = f'https://api.spotify.com/v1/search?q={q}&type=track&market=KR&limit=1'
        #         headers = {
        #             'Authorization': 'Bearer '+access_token
        #         }
        #         response_sp = requests.get(url, headers=headers)
        #         if response_sp.status_code == 200:
        #             sp_json = response_sp.json()
        #             artists_sp = []
        #             song_name.append(sp_json['tracks']['items'][0]['name'])
        #             album_name.append(sp_json['tracks']['items'][0]['album']['name'])
        #             album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                    
        #             for j in range(len(sp_json['tracks']['items'][0]['artists'])):
        #                 artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
        #             artist_name.append(', '.join(artists_sp))
            # responsed_data[i]['track_title'] = song_name[i]
            # for k in range(len(responsed_data[i]['artists'])):
            #     responsed_data[i]['artists'][k]['artist_nm'] = artist_name[i][k]
            # responsed_data[i]['album']['title'] = album_name[i]
            # responsed_data[i]['album']['image']['path'] = album_img[i]
        
        # print(song_name[0])
        # print('#')
        # print(album_name[0])
        # print('#')
        # print(album_img[0])
        # print('#')
        # print(artist_name)
        
        for idx, e in enumerate(responsed_data) :
            entity = BugsEntity(**e)
            orm = BugsORM(entity)
            orm.track_name = song_name[idx]
            orm.album_name = album_name[idx]
            orm.img_url = album_img[idx]
            orm.artist_names = artist_name[idx]

            with session_scope() as session :
                session.add(orm)