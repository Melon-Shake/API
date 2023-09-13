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
        parse_track = urllib.parse.unquote(pre_track_title)
        cleaned_track = re.sub(r'\([^)]*\)', '', parse_track)
        if cleaned_track == '이브, 프시케 그리고 푸른 수염의 아내':
                cleaned_track = 'Eve, Psyche & The Bluebeard’s wife'
        elif cleaned_track == 'Seven  - Clean Ver.':
                cleaned_track ='Seven (feat. Latto) (Clean Ver.)'
        elif cleaned_track == '사람 Pt.2 ':
                cleaned_track = 'People Pt.2 (feat. IU)'
        
        pre_album_title = item['ALBUMNAME']
        parse_album = urllib.parse.unquote(pre_album_title)
        cleaned_album = re.sub(r'\([^)]*\)', '', parse_album)
        
        artists = item.get('ARTISTLIST')
        artist_pre = []
        for artist in artists:
            artist_nm = artist['ARTISTNAME']
            parse_artist = urllib.parse.unquote(artist_nm)
            cleaned_artist = re.sub(r'\([^)]*\)', '', parse_artist)
            if cleaned_artist == '#안녕':
              cleaned_artist = urllib.parse.quote(parse_artist)
            artist_pre.append(artist_nm)
            
        entries[index] = [cleaned_track, cleaned_artist, cleaned_album]
    # print(entries)
    # print(len(entries))
    
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
            artist_name.append(artists_sp)
    responsed_data[i]['SONGNAME'] = song_name[i]
    responsed_data[i]['ARTISTLIST'] = [ dict(ARTISTID=x.get('ARTISTID'),ARTISTNAME=artists_sp[i]) for i, x in enumerate(responsed_data[i]['ARTISTLIST'])]
    responsed_data[i]['ALBUMNAME'] = album_name[i]
    responsed_data[i]['ALBUMIMG'] = album_img[i]
  # print(responsed_data)
    
  for item in responsed_data:
    entity = ChartMelon(**item)
    orm = MelonORM(entity)

    with session_scope() as session :
      session.add(orm)