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
        for itme in responsed_data:
            for index, item in enumerate(responsed_data):
                # 제목 디코딩
                pre_track_title = item['SONG_NAME']
                track_title = urllib.parse.unquote(pre_track_title)
                
                # 아티스트 디코딩
                pre_artists = item.get('ARTIST_NAME')
                artists = urllib.parse.unquote(pre_artists)  # URL 디코딩

                # 앨범제목
                pre_album = item['ALBUM_NAME']
                album = urllib.parse.unquote(pre_album)
                entries[index+1] = [track_title, artists, album]
        print(entries)
                
        # for i in range(len(responsed_data)):

        #     q = responsed_data[i]['SONG_NAME'] +' '+ responsed_data[i]['ARTIST_NAME'] + ' ' + responsed_data[i]['ALBUM_NAME']
        #     url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
        #     headers = {
        #         'Authorization': 'Bearer '+access_token
        #     }
        #     response_sp = requests.get(url, headers=headers)
        #     if response_sp.status_code == 200:
        #         sp_json = response_sp.json()
        #         return_data ={}
        #         artists = []
        #         song_name.append(sp_json['tracks']['items'][0]['name'])
        #         album_name.append(sp_json['tracks']['items'][0]['album']['name'])
        #         album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                
        #         for j in range(len(sp_json['tracks']['items'][0]['artists'])):
        #             artists.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
        #         artist_name.append(artists)
        #     else:
        #         print(f'{i} : {response_sp.status_code}')

        # print(len(responsed_data))
        # print(len(song_name))
        # print(song_name[0])
        # print(song_name[98])
        
        
        # print(artist_name)
        # print(album_name)
        # print(len(responsed_data))

        
        # print(f"곡 : {len(song_name)}   가수 : {len(artist_name)}    앨범 : {len(album_name)}")
        # for i in range(len(responsed_data)):
        #     responsed_data[i]['SONG_NAME'] = song_name[i]
        #     responsed_data[i]['ARTIST_NAME'] = artist_name[i]
        #     responsed_data[i]['ALBUM_NAME'] = album_name[i]
        #     responsed_data[i]['ALBUM_IMG_PATH'] = album_img[i]
        
        # print(responsed_data)
        # for e in responsed_data :
            # entity = ChartGenie(**e)
            # orm = ChartGenieORM(entity)
# 
            # with session_scope() as session :
                # session.add(orm)
# 
    # else : print(response.status_code)