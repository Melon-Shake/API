import requests
import sys
import os, urllib.parse
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
            track_title = item['track_title']
            album_title = item['album']['title']
            artists = item.get('artists')
            artist_pre = []
            for artist in artists:
                artist_nm = artist['artist_nm']
                artist_pre.append(artist_nm)
            entries[index] = [track_title, artist_pre, album_title]
        # {1: ['Smoke (Prod. Dynamicduo, Padi)', ['다이나믹 듀오', '이영지'], '스트릿 우먼 파이터2(SWF2) 계급미션'],}
        
        for i in range(len(responsed_data)):
            artists = ' '.join(entries[i][1])
            q = entries[i][0] + " " + artists + entries[i][2]

            url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
            headers = {
                'Authorization': 'Bearer '+access_token
            }
            response_sp = requests.get(url, headers=headers)
            if response_sp.status_code == 200:
                sp_json = response_sp.json()
                return_data ={}
                artists_sp = []
                # print(sp_json['tracks']['items'][0]['name'])
                song_name.append(sp_json['tracks']['items'][0]['name'])
                album_name.append(sp_json['tracks']['items'][0]['album']['name'])
                album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])

                for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                    artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
                artist_name.append(artists_sp)
            else:
                print(f'{i} : {response_sp.status_code}')

        print(len(responsed_data))
        print(len(song_name))
        
        # for x in responsed_data :
        #     entity = BugsEntity(**x)
        #     orm = BugsORM(entity)

        #     with session_scope() as session :
        #         session.add(orm)