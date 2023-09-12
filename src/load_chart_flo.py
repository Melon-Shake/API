import requests
import sys
import os, urllib.parse
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
            track_title = item['name']
            album_title = item['album']['title']
            artists = item.get('artistList')
            artist_pre = []
            for artist in artists:
                artist_nm = artist['name']
                artist_pre.append(artist_nm)
            entries[index] = [track_title, artist_pre, album_title]
            
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
                song_name.append(sp_json['tracks']['items'][0]['name'])
                album_name.append(sp_json['tracks']['items'][0]['album']['name'])
                album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                # 
                for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                    artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
                artist_name.append(artists_sp)
            else:
                print(f'{i} : {response_sp.status_code}')
        # for i, e in enumerate(parsed_data) :
        #     entity = ChartFlo(**e)
        #     orm = ChartFloORM(i,entity)
            
        #     with session_scope() as session :
        #         session.add(orm)