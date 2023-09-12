import requests
import sys
import os, urllib.parse
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from update_token import return_token
from model.chart_genie import ChartGenie #, ChartGenieORM
from model.database import session_scope

access_token = return_token()

def process_sp_json(sp_json):
    for e in sp_json:
        entity = ChartGenie(**e)
        print(entity)

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

        entries = {}

        for index, item in enumerate(responsed_data):
            # 제목 디코딩
            pre_track_title = item['SONG_NAME']
            track_title = urllib.parse.unquote(pre_track_title)
            
            # 아티스트 디코딩
            pre_artists = item.get('ARTIST_NAME')
            bb = pre_artists.replace('(','%28').replace(')','%29')
            artists = urllib.parse.quote(bb) 

            # 앨범제목
            pre_album = item['ALBUM_NAME']
            album = urllib.parse.unquote(pre_album)
            entries[index] = [track_title, artists, album]
        
        for i in range(len(responsed_data)):
            q = entries[i][0]  + " " + entries[i][2]
            print(q)
            url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
            headers = {
                'Authorization': 'Bearer '+access_token
            }
            response_sp = requests.get(url, headers=headers)
            if response_sp.status_code == 200:
                sp_json = response_sp.json().get('tracks').get('items')
                process_sp_json(sp_json)
                
            elif response_sp.status_code == 400 :
                q = entries[i][0] +  " " + entries[i][2] +  " " + entries[i][3]
                url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
                headers = {
                    'Authorization': 'Bearer '+access_token
                }
                response_sp = requests.get(url, headers=headers)
                
                if response_sp.status_code == 200:
                    sp_json = response_sp.json().get('tracks').get('items')
                    process_sp_json(sp_json)
                    
                ###############################################################
                # Done: name, albumname, imagesUrl, artist
                
                # print(type(sp_json[0]['artists'])) # list
                # print(type(sp_json[0]['artists'][0])) # dict
                # print(type(sp_json[0]['artists'][0]['name'])) # str
                # print(type(sp_json[0]['album']['images'][0]['url'])) # dict
                
                ###############################################################
                
                # for j in range(len(sp_json['tracks']['items'][0]['artists'])):
                #     artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
            
                #     artist_name.append(artists_sp)
                
                
                

                
                # print(data_type_counts)
                    # print(e)
                    # entity = ChartGenie(**e)
                
        #         artists_sp = []

        #         song_name.append(sp_json['tracks']['items'][0]['name'])
        #         album_name.append(sp_json['tracks']['items'][0]['album']['name'])
        #         album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
                
        #         for j in range(len(sp_json['tracks']['items'][0]['artists'])):
        #             artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
                    
        #         artist_name.append(artists_sp)
                
        #     elif response_sp.status_code != 200 :
        #         q = entries[i][0] + " " + entries[i][1]
        #         url = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'
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
                
                
        #         else: print(f'{i} : {response_sp.status_code}')

        # print(f"곡 : {(song_name)}   가수 : {(artist_name)}    앨범 : {(album_name)}")
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