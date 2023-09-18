import requests
import sys
import os, urllib.parse
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from get_token import return_token
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
    Realtime = 'realtime' 
    headers = {"User-Agent": _USER_AGENT}
    data = {"svc_type": Domestic, "period_tp": Realtime,"size":100,}
    response = requests.post(_CHART_API_URL, headers=headers, data=data)
    
    if response.status_code == 200 :
        responsed_data = response.json().get('list')
        song_name = []
        song_ids = []
        artist_name = []
        artist_ids = []
        album_name = []
        album_ids = []
        album_img = []

        entries = {}
        for index, item in enumerate(responsed_data):
            
            # 노래제목
            pre_track_title = item['track_title']
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

            
            # 아티스트
            pre_artists = item.get('artists')
            artist_pre = []
            for artist in pre_artists:
                artist_nm = artist['artist_nm']
                if artist_nm == '#안녕':
                    artist_nm = urllib.parse.quote(artist_nm)
                artist_pre.append(artist_nm)
            artists = ','.join(artist_pre)
            
            pre_album = item['album']['title']
            album = urllib.parse.unquote(pre_album)
            
            entries[index] = [pre_track_title, artists, pre_album]
                    
        for i in range(len(entries)):
            q = entries[i][0] +' '+ entries[i][1]
            url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
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
            entity = BugsEntity(**e)
            orm = BugsORM(entity)
            orm.track_name = song_name[idx]
            orm.track_id = song_ids[idx]
            orm.artist_names = ','.join(artist_name[idx])
            orm.artist_ids = artist_ids[idx]
            orm.album_name = album_name[idx]
            orm.album_id = album_ids[idx]
            orm.img_url = album_img[idx]
            
            with session_scope() as session :
                session.add(orm)