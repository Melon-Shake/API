import sys
import os
import re
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import urllib.parse

from update_token import return_token
from model.database import session_scope
from model.chart_melon import ChartMelon, MelonORM
import requests

access_token = return_token()

if __name__ == '__main__':
  _APP_VERSION = "6.5.8.1"
  _CP_ID = "AS40"
  _USER_AGENT = f"{_CP_ID}; Android 13; {_APP_VERSION}; sdk_gphone64_arm64"
  _CHART_API_URL = f"https://m2.melon.com/m6/chart/ent/songChartList.json?cpId={_CP_ID}&cpKey=14LNC3&appVer={_APP_VERSION}"
  headers = {"User-Agent": _USER_AGENT}
  
  response = requests.get(_CHART_API_URL,headers=headers)
  
  if response.status_code == 200 :
    response = response.json()
    responsed_data = response['response']['SONGLIST']
    
    song_name = []
    artist_name = []
    album_name = []
    album_img = []

    entries = {}
    for index, item in enumerate(responsed_data):
        pre_track_title = item['SONGNAME']
        # pre_track_title = urllib.parse.unquote(pre_track_title)
        pre_track_title = pre_track_title.replace("-", "")
        pre_track_title = pre_track_title.replace("Prod. by", "Prod.")

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
        
        #
        pre_artists = item.get('ARTISTLIST')
        artists = []
        for artist in pre_artists:
            artist_nm = artist['ARTISTNAME']
            parse_artist = urllib.parse.unquote(artist_nm)
            if parse_artist == '#안녕':
              parse_artist = urllib.parse.quote(parse_artist)
            artists.append(parse_artist)
        artists = ','.join(artists)
            
        pre_album_title = item['ALBUMNAME']
        pre_album_title = urllib.parse.unquote(pre_album_title)

            
        entries[index] = [pre_track_title, artists, pre_album_title]
    # print(entries)
    
  for i in range(len(entries)):
    q = entries[i][0] + " " + entries[i][1]
    # print(q)
    url = f'https://api.spotify.com/v1/search?q={q}&type=track&maket=KR&limit=1'
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
    # elif response_sp.status_code != 200 :
    #     q = entries[i][0] + " " + entries[i][1]+ " " + entries[i][2]
    #     url = f'https://api.spotify.com/v1/search?q={q}&type=track&market=KR&limit=1'
    #     headers = {
    #         'Authorization': 'Bearer '+access_token
    #     }
    #     response_sp = requests.get(url, headers=headers)
    #     if response_sp.status_code == 200:
    #         sp_json = response_sp.json()
    #         artists_sp = []
    #         song_name.append(sp_json['tracks']['items'][0]['name'])
    #         album_name.append(sp_json['tracks']['items'][0]['album']['name'])
    #         album_img.append(sp_json['tracks']['items'][0]['album']['images'][0]['url'])
            
    #         for j in range(len(sp_json['tracks']['items'][0]['artists'])):
    #             artists_sp.append(sp_json['tracks']['items'][0]['artists'][j]['name'])
            # artist_name.append(artists_sp)
    # responsed_data[i]['SONGNAME'] = song_name[i]
    # responsed_data[i]['ARTISTLIST'] = [ dict(ARTISTID=x.get('ARTISTID'),ARTISTNAME=artists_sp[i]) for i, x in enumerate(responsed_data[i]['ARTISTLIST'])]
    # responsed_data[i]['ALBUMNAME'] = album_name[i]
    # responsed_data[i]['ALBUMIMG'] = album_img[i]
  # print(song_name[0])
  # print(album_img[0])
  # print(album_name[0])
  # print(artist_name[0])
  
  for idx, item in enumerate(responsed_data):
    entity = ChartMelon(**item)
    orm = MelonORM(entity)
    orm.track_name = song_name[idx]
    orm.artist_names = artist_name[idx]
    orm.album_name = album_name[idx]
    orm.img_url = album_img[idx]

    with session_scope() as session :
      session.add(orm)