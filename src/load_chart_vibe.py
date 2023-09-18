import requests
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import urllib.parse
from model.chart_vibe import VibeEntity, VibeORM
from model.database import session_scope
from get_token import return_token

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
        song_name = []
        song_ids = []
        artist_name = []
        artist_ids = []
        album_name = []
        album_ids = []
        album_img = []
        entries = {}
        
        for index, item in enumerate(responsed_data):
            e = VibeEntity(**item)
            e.trackTitle
            e.album.albumTitle
            e.album.imageUrl
            e.artists
            
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
            
            pre_artist = e.artists
            artists = []
            for artist in pre_artist:
                pre_artist = artist.artistName
                parse_artist = urllib.parse.unquote(pre_artist)  # URL 디코딩
                if parse_artist == '#안녕':
                    parse_artist = urllib.parse.quote(parse_artist)
                artists.append(parse_artist) 
            artists = ','.join(artists)
            entries[index] = [pre_track_title, artists, parse_album]
        
        for i in range(len(entries)):
            q = entries[i][0] + " " + entries[i][1]
            url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
            headers = {
                'Authorization': 'Bearer '+access_token
            }
            response_sp = requests.get(url, headers=headers)
            if response_sp.status_code == 200:
                sp_json = response_sp.json()
                artists_sp_nm = []
                artist_id = []
                song_name.append(sp_json['tracks']['items'][0]['name'])
                song_ids.append(sp_json['tracks']['items'][0]['id'])
                album_name.append(sp_json['tracks']['items'][0]['album']['name'])
                album_ids.append(sp_json['tracks']['items'][0]['album']['id'])
                album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                    artists_sp_nm.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
                    artist_id.append(sp_json['tracks']['items'][0]['artists'][j]['id'])
                artist_name.append(artists_sp_nm)
                artist_ids.append(artist_id)
        
        for idx, e in enumerate(responsed_data):
            entity = VibeEntity(**e)
            orm = VibeORM(entity)
            orm.track_name = song_name[idx]
            orm.track_id = song_ids[idx]
            orm.artist_names = ','.join(artist_name[idx])
            orm.artist_ids = artist_ids[idx]
            orm.album_name = album_name[idx]
            orm.album_id = album_ids[idx]
            orm.img_url = album_img[idx]

            with session_scope() as session :
                session.add(orm)