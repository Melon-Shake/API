import requests
import sys
import os, urllib.parse, re
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from update_token import return_token
from model.chart_flo import ChartFlo, ChartFloORM
from model.database import session_scope

access_token = return_token()

if __name__ == '__main__':

    response = requests.get("https://api.music-flo.com/display/v1/browser/chart/1/list?mixYn=N"
                      ,headers = {"User-Agent": "okhttp/4.9.2",
                                  "x-gm-app-name":"FLO",
                                   "x-gm-app-version": ""
                                }
                      )

    if response.status_code == 200 :
        response = response.json()
        responsed_data = response.get('data').get('trackList')
        
        song_name = []
        artist_name = []
        album_name = []
        album_img = []
        
        entries = {}
        for index, item in enumerate(responsed_data):
            
            # 제목 디코딩
            pre_track_title = item['name']
            track_title = urllib.parse.unquote(pre_track_title)
            cleaned_track = re.sub(r'\([^)]*\)', '', track_title)
            
            # 예외 처리
            if cleaned_track == '이브, 프시케 그리고 푸른 수염의 아내':
                cleaned_track = 'Eve, Psyche & The Bluebeard’s wife'
            elif cleaned_track == 'Seven  - Clean Ver.':
                cleaned_track ='Seven (feat. Latto) (Clean Ver.)'
            elif cleaned_track == '사람 Pt.2 ':
                cleaned_track = 'People Pt.2 (feat. IU)'
            
            
            # 아티스트 디코딩
            pre_artist = item.get('artistList')
            artist_pre = []
            
            for artist in pre_artist:
                artist_nm = artist['name']
                artists = urllib.parse.unquote(artist_nm)
                
                if artists == '#안녕':
                    artists_excep = urllib.parse.quote(artists)
                    artist_pre.append(artists_excep)
                else :
                    cleaned_artist = re.sub(r'\([^)]*\)', '', artists)
                    artist_pre.append(cleaned_artist)
                    
            # 앨범 제목
            pre_album = item['album']['title']
            album = urllib.parse.unquote(pre_album)
            cleaned_album = re.sub(r'\([^)]*\)', '', album)
            
            entries[index] = [cleaned_track, artist_pre, cleaned_album]
        for i in range(len(responsed_data)):
            var_artists = ' '.join(entries[i][1])
            q = entries[i][0] + " " + var_artists

            url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
            headers = {
                'Authorization': 'Bearer '+access_token
            }
            response_sp = requests.get(url, headers=headers)
            if response_sp.status_code == 200:
                sp_json = response_sp.json()
                return_data ={}
                artists_sp = []
                song_name.append(sp_json['tracks']['items'][0]['name'])
                album_name.append(sp_json['tracks']['items'][0]['album']['name'])
                album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                
                for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                    artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
                artist_name.append(', '.join(artists_sp))
            elif response_sp.status_code != 200 :
                q = entries[i][0] + " " + var_artists + " " + entries[i][2]
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
                    
            responsed_data[i]['name'] = song_name[i]
            responsed_data[i]['artistList'][0]['name'] = artist_name.pop()
            responsed_data[i]['album']['title'] = album_name[i]
            responsed_data[i]['album']['imgList'][0]['url'] = album_img[i]
                    
        for e in responsed_data :
            entity = ChartFlo(**e)
            orm = ChartFloORM(i,entity)
            
            with session_scope() as session :
                session.add(orm)