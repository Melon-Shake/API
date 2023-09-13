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
            track_title = urllib.parse.unquote(pre_track_title)
            cleaned_track = re.sub(r'\([^)]*\)', '', track_title)
            
            # 예외 처리ㅔ
            if cleaned_track == '이브, 프시케 그리고 푸른 수염의 아내':
                cleaned_track = 'Eve, Psyche & The Bluebeard’s wife'
            elif cleaned_track == 'Seven  - Clean Ver.':
                cleaned_track ='Seven (feat. Latto) (Clean Ver.)'
            elif cleaned_track == '사람 Pt.2 ':
                cleaned_track = 'People Pt.2 (feat. IU)'
                
            
            # 아티스트 디코딩
            pre_artists = item.get('artists')
            artist_pre = []
            
            for artist in pre_artists:
                artist_nm = artist['artist_nm']
                artists = urllib.parse.unquote(artist_nm)
                
                if artists == '#안녕':
                    artists_excep = urllib.parse.quote(artist_nm)
                    artist_pre.append(artists_excep)
                else:
                    cleaned_artist = re.sub(r'\([^)]*\)', '', artists)
                    artist_pre.append(cleaned_artist)
            
            # 앨범제목    
            pre_album = item['album']['title']
            album = urllib.parse.unquote(pre_album)
            cleaned_album = re.sub(r'\([^)]*\)', '', album)
            
            entries[index] = [cleaned_track, artist_pre, cleaned_album]

        # {1: ['Smoke (Prod. Dynamicduo, Padi)', ['다이나믹 듀오', '이영지'], '스트릿 우먼 파이터2(SWF2) 계급미션'],}
        
        for i in range(len(responsed_data)):
            artists = ' '.join(entries[i][1])
            q = entries[i][0] + " " + artists

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

            responsed_data[i]['track_title'] = song_name[i]
            responsed_data[i]['artists'][0]['artist_nm'] = artist_name.pop()
            responsed_data[i]['album']['title'] = album_name[i]
            responsed_data[i]['album']['image']['path'] = album_img[i]

        
        for x in responsed_data :
            entity = BugsEntity(**x)
            orm = BugsORM(entity)

            with session_scope() as session :
                session.add(orm)